# GitHub Actions para credenciais e automação social — findings 2026

## Secrets

O GitHub permite secrets em nível de repositório, ambiente ou organização. Para criar secrets no repositório é necessário acesso de escrita; para secrets de Environment são necessários privilégios de administração conforme o tipo de repositório [1]. Os secrets são referenciados pelo contexto `secrets` dentro do workflow e não ficam disponíveis automaticamente para workflows disparados por forks ou Dependabot [1].

A recomendação para KTD é usar um Environment chamado `production-social`, com secrets separados por plataforma e permissões mínimas. Não usar valores em linha de comando, URLs, artefatos, logs ou arquivos versionados. Quando um valor sensível não for um GitHub Secret, o workflow deve mascará-lo explicitamente [1].

Nomes previstos:

- `KTD_INSTAGRAM_ACCESS_TOKEN`
- `KTD_INSTAGRAM_APP_SECRET`
- `KTD_INSTAGRAM_USER_ID`
- `KTD_META_WEBHOOK_VERIFY_TOKEN`
- `KTD_TIKTOK_ACCESS_TOKEN`
- `KTD_TIKTOK_CLIENT_SECRET`
- `KTD_TIKTOK_CLIENT_KEY`
- `KTD_TIKTOK_REFRESH_TOKEN`
- `KTD_SOCIAL_API_BASE_URL`

`KTD_INSTAGRAM_USER_ID` e `KTD_SOCIAL_API_BASE_URL` não são secrets estritos, mas podem permanecer como Environment variables para separar configuração de produção.

## Environments

Jobs que referenciam um Environment só recebem seus Environment secrets depois que regras configuradas forem satisfeitas. O GitHub permite required reviewers, wait timers, restrição de branches/tags e regras de proteção de deployment [2]. No plano gratuito, Environment protection rules e secrets têm limitações para repositórios privados; em repositórios públicos estão disponíveis [2].

Para a autonomia híbrida de KTD, criar pelo menos:

| Environment | Uso | Proteção sugerida |
|---|---|---|
| `social-staging` | dry-run, validação de tokens e testes de webhook | nenhum secret de publicação pública; branch de teste |
| `production-social` | publicação real, refresh e webhooks | branch/tag protegida, wait timer e optional reviewer para primeira ativação |

Mesmo quando a operação diária for autônoma, o Environment pode ser protegido apenas para deploy/alteração de infraestrutura; a política de conteúdo do agente continua no próprio orquestrador.

## OIDC

OIDC permite que GitHub Actions autentique no provedor de nuvem sem armazenar credenciais de longa duração como GitHub Secrets. O provedor deve confiar no issuer do GitHub e restringir claims para impedir que repositórios não confiáveis obtenham tokens. O workflow precisa de `permissions: id-token: write` e de uma action oficial ou troca equivalente [3].

OIDC não substitui os tokens OAuth da Meta/TikTok. Ele pode substituir a chave longa usada para o GitHub Actions acessar o ambiente persistente, registry, secret manager ou serviço de deploy. Os tokens de publicação ainda devem ser armazenados no secret manager e renovados no backend.

## Agendamento

GitHub Actions pode disparar workflows por `schedule`, mas o schedule roda a partir do default branch e não deve ser usado como receptor de webhooks. O GitHub registra que schedules podem sofrer atrasos em períodos de alta carga; o primeiro passo de publicação deve verificar idempotência e estado antes de tentar uma ação externa [4].

Para KTD, o schedule é adequado para:

- renovar tokens antes de expirar;
- consultar status de publicação como fallback;
- coletar insights em baixa frequência;
- despachar campanhas previamente aprovadas no SQLite.

Webhooks Meta/TikTok devem chegar diretamente ao serviço HTTPS persistente. Um workflow agendado pode processar eventos persistidos, mas não deve substituir o endpoint público.

## Referências oficiais

[1]: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions — GitHub Docs, Using secrets in GitHub Actions.

[2]: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment — GitHub Docs, Managing environments for deployment.

[3]: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers — GitHub Docs, Configuring OpenID Connect in cloud providers.

[4]: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule — GitHub Docs, Events that trigger workflows — schedule.

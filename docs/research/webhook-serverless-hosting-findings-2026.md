# Receptor HTTPS serverless para webhooks — findings 2026

## Cloud Run

Cloud Run é uma plataforma gerenciada que executa código ou containers sem exigir gerenciamento de cluster. Um Cloud Run service fornece endpoint HTTPS estável, TLS gerenciado, autoscaling e possibilidade de domínio customizado. Instâncias são stateless e podem ser removidas quando o tráfego cai; o comportamento de scale-to-zero reduz operação contínua, mas o primeiro request pode sofrer cold start [1].

O filesystem do container é descartável. Eventos recebidos precisam ser persistidos em datastore externo, como Cloud SQL, Firestore, Storage ou fila. Cloud Run também integra com Cloud Tasks e Pub/Sub para processamento assíncrono [1].

## AWS Lambda / API Gateway

A AWS documenta Lambda Function URLs como uma forma simples de criar um endpoint HTTPS para webhooks leves e orientados a eventos. Para autenticação e validação mais avançadas, a AWS recomenda API Gateway. A função deve validar HMAC, persistir o evento e responder rapidamente [2].

API Gateway pode funcionar como front door HTTP, transformar requisições em eventos para Lambda e oferecer autenticação, monitoramento, rate limits e integração com outros endpoints. HTTP APIs são a opção mais simples e de menor preço quando os recursos avançados de REST API não são necessários [3].

## Aplicação ao KTD Social Orchestrator

A melhor separação é: receptor HTTPS stateless valida assinatura e handshake, calcula `event_id`, persiste o payload mínimo e coloca o evento em uma fila; uma função/worker separado chama o orquestrador social, atualiza o status e aplica retries/backoff. GitHub Actions pode fazer deploy, health checks e manutenção, mas não deve ser o receptor HTTPS.

O FastAPI existente pode ser empacotado como Cloud Run service ou adaptado para uma função serverless. SQLite local não deve ser a fonte de verdade em ambiente serverless, pois o filesystem é efêmero. A persistência deve migrar para um banco/kv/queue gerenciado ou para o armazenamento persistente do serviço escolhido.

## Referências

[1]: https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run — Google Cloud, What is Cloud Run.

[2]: https://docs.aws.amazon.com/lambda/latest/dg/urls-webhook-tutorial.html — AWS Lambda, Tutorial: Creating a webhook endpoint using a Lambda function URL.

[3]: https://docs.aws.amazon.com/serverless/latest/devguide/starter-apigw.html — AWS, Get started with API Gateway.

# Guia de Estudo - Sistema ArecoID

Este guia resume os principais conceitos, tecnologias e definicoes que voce deve estudar para trabalhar no projeto ArecoID.

O ArecoID, segundo a documentacao analisada, parece ser um sistema backend em .NET/C#, organizado com Clean Architecture, DDD, CQRS, Entity Framework Core, Keycloak, RabbitMQ e padroes como Outbox Pattern, Result Pattern e Dependency Injection.

## 1. Visao geral da arquitetura

O sistema e dividido em camadas:

```text
API
 v
Application
 v
Domain
 ^
Infrastructure
```

A ideia principal e separar responsabilidades.

## 2. Domain Layer

A camada de dominio e o coracao do sistema.

Ela contem:

- entidades de negocio;
- regras de negocio;
- value objects;
- interfaces;
- excecoes de dominio;
- tipos como `Result`, `Error` e `PagedResult`.

Essa camada nao deve depender de banco de dados, API, RabbitMQ, Keycloak ou frameworks externos.

Uma forma simples de pensar:

> O que e uma conta, usuario, permissao ou regra de autenticacao no negocio?

### Entidades

Entidades sao objetos com identidade propria.

Exemplos possiveis:

- `User`;
- `Tenant`;
- `Role`;
- `Permission`.

Mesmo que os dados mudem, a entidade continua sendo a mesma.

### Value Objects

Value objects sao objetos definidos pelos seus valores, nao por identidade.

Exemplos:

- `Email`;
- `Cpf`;
- `Address`;
- `Money`.

Se dois value objects possuem os mesmos valores, eles sao considerados equivalentes.

### BaseEntity

Segundo a documentacao, todas as entidades herdam de `BaseEntity` e possuem:

- `ExternalKey`: identificador publico usando Guid v7;
- `DeletedAt`: campo usado para soft delete;
- campos de auditoria de criacao e atualizacao.

## 3. Application Layer

A camada de aplicacao contem os casos de uso.

Exemplos:

- criar usuario;
- autenticar usuario;
- alterar senha;
- listar usuarios;
- enviar evento de cadastro.

Essa camada orquestra o fluxo de negocio, valida dados de entrada e coordena chamadas ao dominio e a infraestrutura.

### Vertical Slices

A documentacao indica organizacao por features, tambem conhecida como vertical slices.

Em vez de separar tudo apenas por tipo tecnico, como:

```text
Controllers/
Services/
Repositories/
Validators/
```

o projeto tende a organizar por funcionalidade:

```text
Users/
  CreateUser/
  GetUserById/
  ListUsers/
```

Isso ajuda a localizar tudo que pertence a uma mesma feature.

## 4. CQRS

CQRS significa Command Query Responsibility Segregation.

A ideia e separar operacoes de escrita de operacoes de leitura.

### Commands

Commands representam uma intencao de negocio que altera estado.

Exemplos:

- `CreateUserCommand`;
- `UpdatePasswordCommand`;
- `DeleteTenantCommand`.

Um ponto importante da documentacao:

> Command representa uma intencao de negocio, nao apenas um conjunto de dados.

Ou seja, um command nao deve ser visto apenas como um DTO. Ele representa uma acao.

A documentacao tambem reforca:

> Prefira composicao ao inves de heranca.

Isso significa evitar hierarquias complexas de classes quando objetos compostos resolvem melhor o problema.

### Queries

Queries representam consultas.

Exemplos:

- `GetUserByIdQuery`;
- `ListUsersQuery`;
- `SearchTenantsQuery`.

Queries nao devem alterar estado.

### Handlers

Handlers executam commands ou queries.

Exemplo conceitual:

```text
Controller recebe HTTP
 v
Cria Command ou Query
 v
Dispatcher envia para Handler
 v
Handler executa o caso de uso
 v
Retorna Result
```

### Dispatcher

O dispatcher centraliza o envio de commands e queries para os handlers corretos.

Ele evita que controllers conhecam diretamente todos os handlers.

## 5. Infrastructure Layer

A camada de infraestrutura contem os detalhes tecnicos.

Ela implementa:

- acesso a dados com Entity Framework Core;
- integracoes com Keycloak;
- integracoes com RabbitMQ;
- envio de e-mail via SMTP;
- background services;
- implementacao de repositorios;
- implementacao do Outbox Pattern.

Uma forma simples de pensar:

> Como eu salvo isso no banco?
> Como eu publico uma mensagem no RabbitMQ?
> Como eu chamo o Keycloak?

Essas respostas normalmente ficam na Infrastructure.

## 6. API Layer

A camada API e a camada exposta para o mundo externo.

Ela contem:

- controllers REST;
- endpoints HTTP;
- tratamento de erro HTTP;
- autenticacao JWT;
- documentacao OpenAPI/Swagger;
- validacao basica de entrada.

Exemplos de endpoints:

```http
POST /users
GET /users/{id}
POST /auth/login
```

## 7. Fluxo tipico de uma requisicao

Exemplo: criar usuario.

```text
1. Cliente chama POST /users
2. Controller recebe a requisicao
3. Controller monta um CreateUserCommand
4. Dispatcher envia para o handler correto
5. Handler valida regras
6. Handler usa entidades do Domain
7. Handler chama repositorio
8. Infrastructure salva com EF Core
9. Talvez cria evento na Outbox
10. Background service publica evento no RabbitMQ
11. API retorna resposta HTTP
```

## 8. Result Pattern

O Result Pattern evita usar excecoes para todo erro esperado.

Em vez disso, o sistema retorna um objeto indicando sucesso ou falha.

Exemplo conceitual:

```csharp
Result.Success(value)
Result.Failure(error)
```

Esse padrao ajuda a tratar erros previsiveis, como:

- usuario nao encontrado;
- e-mail invalido;
- permissao negada;
- senha incorreta;
- conflito de dados.

E importante diferenciar:

- erro esperado de negocio;
- excecao inesperada do sistema.

## 9. Entity Framework Core

Entity Framework Core e o ORM usado para acessar o banco de dados.

Voce deve estudar:

- `DbContext`;
- `DbSet`;
- migrations;
- relacionamentos;
- tracking;
- queries com LINQ;
- eager loading com `Include`;
- transacoes;
- configuracao de entidades;
- soft delete;
- auditoria.

## 10. Soft Delete

Soft delete significa exclusao logica.

Em vez de apagar o registro fisicamente do banco, o sistema marca o registro como deletado.

Exemplo:

```csharp
DeletedAt = DateTime.UtcNow;
```

Assim, o registro continua no banco, mas normalmente nao aparece nas consultas.

Voce precisa prestar atencao para nao listar registros deletados por engano.

## 11. Auditoria

Campos de auditoria ajudam a saber quem criou, alterou ou removeu logicamente um registro.

Exemplos:

```text
CreatedAt
CreatedBy
UpdatedAt
UpdatedBy
DeletedAt
```

## 12. Guid v7 e ExternalKey

O sistema usa `ExternalKey` com Guid v7.

Guid tradicional costuma ser aleatorio. Guid v7 e ordenavel por tempo, o que ajuda em banco de dados e em ordenacao cronologica.

Provavelmente existe:

- um ID interno, tecnico ou numerico;
- um `ExternalKey` publico exposto na API.

Boa pratica:

> Evite expor IDs internos se o sistema usa `ExternalKey` como identificador publico.

## 13. Keycloak, OpenID Connect e JWT

O sistema usa Keycloak para autenticacao.

### Keycloak

Keycloak e um servidor de identidade e autenticacao.

Ele gerencia:

- usuarios;
- senhas;
- clients;
- realms;
- roles;
- grupos;
- tokens.

### OpenID Connect

OpenID Connect e um protocolo de autenticacao baseado em OAuth 2.0.

Ele responde a pergunta:

> Quem e o usuario?

### JWT Bearer Token

JWT e um token usado para acessar APIs.

Normalmente e enviado assim:

```http
Authorization: Bearer eyJ...
```

O backend valida o token e identifica o usuario.

### Refresh Token

Refresh token e usado para renovar o access token sem fazer login novamente.

## 14. RabbitMQ

RabbitMQ e usado para mensageria assincrona.

Serve para tarefas que nao precisam acontecer imediatamente dentro da requisicao HTTP.

Exemplos:

- enviar e-mail;
- sincronizar dados;
- publicar evento de usuario criado;
- processar operacao demorada;
- comunicar outro servico.

Conceitos importantes:

- exchange;
- queue;
- routing key;
- publisher;
- consumer;
- acknowledgement;
- retry;
- dead-letter queue.

## 15. Outbox Pattern

O Outbox Pattern e importante para garantir consistencia eventual ao publicar mensagens.

Problema comum:

```text
1. Salvar usuario no banco
2. Publicar mensagem no RabbitMQ
```

E se salvar no banco funcionar, mas publicar no RabbitMQ falhar?

O Outbox Pattern resolve isso salvando a mensagem no banco junto com a transacao principal.

Fluxo:

```text
Salva entidade
Salva evento na tabela Outbox
Commit no banco
Background service le Outbox
Publica no RabbitMQ
Marca como publicado
```

Isso aumenta a confiabilidade do sistema.

## 16. Dependency Injection

Dependency Injection conecta interfaces e implementacoes.

Exemplo:

```csharp
services.AddScoped<IUserRepository, UserRepository>();
```

Assim uma classe pode depender da abstracao:

```csharp
IUserRepository
```

E nao da implementacao concreta:

```csharp
UserRepository
```

Isso facilita testes, manutencao e troca de tecnologia.

## 17. Middleware

No ASP.NET Core, middleware e uma etapa no pipeline HTTP.

Exemplo:

```text
Request
 v
Exception Middleware
 v
Authentication
 v
Authorization
 v
Rate Limiting
 v
Controller
 v
Response
```

Voce deve estudar:

- autenticacao;
- autorizacao;
- tratamento global de erros;
- logs;
- rate limiting;
- CORS;
- Swagger/OpenAPI.

## 18. Rate Limiting

A documentacao cita:

```text
60 requisicoes por minuto
fila de 5 requisicoes
```

Isso limita abuso da API.

Quando o limite e excedido, o usuario pode receber:

```http
429 Too Many Requests
```

## 19. Principios SOLID

### SRP - Single Responsibility Principle

Cada classe deve ter uma responsabilidade principal.

No projeto:

- cada handler deve ter uma unica responsabilidade;
- controllers apenas roteiam requisicoes;
- services devem ser focados em uma tarefa especifica.

### OCP - Open/Closed Principle

O sistema deve ser aberto para extensao e fechado para modificacao.

No projeto, novas features podem ser adicionadas com novos handlers, sem alterar muito codigo existente.

### LSP - Liskov Substitution Principle

Classes derivadas devem poder substituir suas classes base sem quebrar comportamento.

### ISP - Interface Segregation Principle

Interfaces devem ser especificas e coesas.

Evite interfaces grandes que obriguem classes a implementar metodos que nao usam.

### DIP - Dependency Inversion Principle

Modulos de alto nivel nao devem depender de detalhes de baixo nivel.

No projeto:

- Domain nao depende de Infrastructure;
- Application depende de abstracoes;
- Infrastructure implementa essas abstracoes;
- o container de DI conecta tudo.

## 20. Ordem sugerida de estudo

Prioridade recomendada:

1. C# moderno
2. ASP.NET Core Web API
3. Entity Framework Core
4. Clean Architecture
5. DDD basico
6. CQRS com Commands, Queries e Handlers
7. Dependency Injection
8. JWT, OAuth2, OpenID Connect e Keycloak
9. RabbitMQ
10. Outbox Pattern
11. Testes automatizados em .NET

## 21. Checklist pratico para trabalhar em uma feature

Ao abrir uma feature no codigo, tente responder:

- Qual e a entidade principal?
- Isso e uma leitura ou escrita?
- Se for escrita, existe um Command?
- Se for leitura, existe uma Query?
- Onde esta o Handler?
- Qual repository e usado?
- A regra pertence ao Domain ou Application?
- Existe validacao?
- Existe retorno com `Result`?
- A API expoe ID interno ou `ExternalKey`?
- Precisa publicar evento?
- Precisa gravar na Outbox?
- Tem teste cobrindo o comportamento?

## 22. Glossario rapido

| Termo | Significado |
| --- | --- |
| Clean Architecture | Separacao do sistema em camadas independentes |
| DDD | Modelagem focada no dominio de negocio |
| Entity | Objeto com identidade |
| Value Object | Objeto definido pelo valor |
| Command | Intencao de alterar estado |
| Query | Intencao de consultar dados |
| Handler | Classe que executa command/query |
| Dispatcher | Encaminha command/query para o handler |
| Repository | Abstracao de acesso a dados |
| EF Core | ORM do .NET |
| Keycloak | Servidor de autenticacao |
| JWT | Token de acesso |
| RabbitMQ | Sistema de filas/mensageria |
| Outbox | Padrao para publicar mensagens com seguranca |
| Middleware | Etapa do pipeline HTTP |
| DI | Injecao de dependencia |
| Soft Delete | Exclusao logica |
| Result Pattern | Retorno estruturado de sucesso/erro |

## 23. Resumo final

Se voce dominar bem C#, ASP.NET Core, Entity Framework Core, Clean Architecture e CQRS, ja conseguira se localizar melhor no projeto.

Depois, aprofunde em Keycloak, RabbitMQ e Outbox Pattern, que sao partes mais avancadas de integracao e infraestrutura.

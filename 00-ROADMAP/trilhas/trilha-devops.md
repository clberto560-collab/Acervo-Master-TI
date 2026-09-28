# Trilha: Automacao / DevOps

**Objetivo:** entregar infraestrutura como codigo, containers e pipelines — o diferencial de empregabilidade.
**Pre-requisito:** Python basico + Linux (senão vira conteudo "decorado").
**Artefato de saida:** playbook Ansible operacional + servico em container + base de CI/CD.

---

## Topicos na ordem

1. Versionamento com Git (comandos do dia a dia, branches, remoto GitHub)
2. Docker: imagem vs container, Dockerfile, volumes, `docker compose` basico
3. Colocar servico em container (ex.: Zabbix, Snort ou nginx)
4. Ansible: inventario, playbook, modulos comuns (user, apt, service, template)
5. Playbook de hardening: usuarios, firewall, atualizacoes, criacao de logs
6. IaC: conceitos e primeiro contato com Terraform (provider, resource, apply)
7. CI/CD: pipeline simple s no GitHub Actions (ex.: validar playbook/script)
8. Cloud basico: AWS/Azure teoria de servicos fundamentais (VPC, EC2/VM, storage)

## Fluxo de estudo

- Cada topico = artefato executavel + nota.
- Ansible: sempre rodar em VM de teste e validar o resultado (nao so "rodou sem error").
- Git: todo artefato deste acervo vai para o GitHub a partir do Dia 1.

## Recursos

- Documentacao oficial Docker (getting started)
- Documentacao Ansible (guia inicial)
- GitHub Skills (github.com/skills)
- Udemy/DIO: cursos de Ansible + Docker basico (use como apoio, nao como fonte unica)

## Checklist de confirmacao

- [ ] Sobe e derruba um container Docker com configuracao propria (Dockerfile)
- [ ] Playbook Ansible cria usuario, instala pacote e ajusta firewall num servidor de teste
- [ ] Reusa o mesmo playbook em 2 maquinas sem editar (inventario)
- [ ] Tem repositório GitHub organizado com README por projeto
- [ ] Inicializa pipeline no GitHub Actions que roda uma validacao PR
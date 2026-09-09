# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] - 09/09/2026

### Added

- Conexão direta com a tabela oficial de eficiência do Inmetro, reunindo mais de 170 modelos 100% elétricos testados no Brasil
- Nova aba com foco no Selo CONPET de alta eficiência e notas gerais concedidas pelo governo
- Gráfico comparando o rendimento do carro elétrico na cidade contra a estrada
- Tela inicial com aviso amigável e passo a passo caso o arquivo de dados ainda precise ser gerado no terminal
- Botão para recarregar o painel com apenas um clique assim que a esteira de dados terminar de rodar

### Changed

- Filtros da barra lateral agora iniciam com as 5 principais marcas e categorias para carregar a tela de forma mais limpa e ágil
- Remoção de estimativas manuais de preço em favor dos dados técnicos oficiais de consumo em Megajoules por quilômetro (MJ/km)
- Atualização do ícone da aplicação para o símbolo de raio

### Fixed

- Correção no carregamento que impedia a tela de atualizar após rodar o comando no terminal devido ao cache antigo

## [1.0.0] - 09/09/2026

### Added

- Painel interativo para explorar modelos de carros 100% elétricos disponíveis no Brasil
- Filtros na barra lateral para buscar por fabricante, modelo de carroceria, preço máximo e autonomia
- Cartões com os principais números do mercado: quantidade de modelos, preço médio e recordista de alcance
- Gráfico comparativo entre preço e autonomia com ficha técnica completa ao passar o mouse
- Gráfico com as marcas líderes em oferta de elétricos com cores por categoria e contagem de modelos
- Gráfico de faixas de preço por categoria com limites de valores e preços medianos
- Tabela com todas as especificações técnicas e botão para baixar a planilha em formato CSV
- Documentação com orientações completas para rodar localmente e publicar na nuvem

# PIM Accessibility — portfólio de Patrícia Magrinho

Site estático publicado com GitHub Pages a partir da branch `main` (pasta raiz):
https://pim-accessibility.github.io/pim.accessibility/

Versão ativa: **v2.2 B (azul e amarelo)**, implementada a partir do Figma
(ficheiro `6kS5wKl0BPQ72f961VNeDH`, nós 57:654 desktop e 57:1576 mobile).

## Estrutura

| Ficheiro | Conteúdo |
|---|---|
| `index.html`, `resume.html` | Página inicial e currículo em inglês |
| `pt/index.html`, `pt/resume.html` | As mesmas páginas em português (pt-PT) |
| `404.html` | Página de erro bilingue (caminhos absolutos para o GitHub Pages) |
| `css/site.css` | Tokens do tema claro/escuro, layout, foco, anotações |
| `js/site.js` | Seletor de tema e botão das anotações (sem dependências) |
| `assets/` | Ícones exportados do Figma e a fonte Atkinson Hyperlegible Next (SIL OFL) |
| `tools/build.py` | Gera as 5 páginas HTML a partir de um só modelo |
| `.nojekyll` | O GitHub Pages serve os ficheiros tal como estão |

## Alterar texto

Edite os dicionários `T` (página inicial) e `R` (currículo) em `tools/build.py` e execute:

    python3 tools/build.py .

## Acessibilidade

Alvo WCAG 2.2 AA, com AAA sempre que aplicável: contraste de texto ≥ 7:1 nos dois temas,
foco visível de 3px, alvos ≥ 44px, reflow a 320px, `lang`/`hreflang` em cada idioma,
link de salto sempre visível. As anotações de acessibilidade são apenas visuais
(conteúdo gerado por CSS com texto alternativo vazio) e podem ser ocultadas.

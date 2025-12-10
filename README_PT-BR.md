[Read this in English](README.md)

<p align="center">
  <a href="https://www.gnu.org/licenses/gpl-3.0"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3"></a>
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.7%2B-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://github.com/rfm-code-dev/DB-Reborn/releases/"><img src="https://img.shields.io/github/downloads/YOUR_USERNAME/YOUR_REPOSITORY/total" alt="GitHub all releases"></a>
  <a href="https://github.com/rfm-code-dev/DB-Reborn/commits/main"><img src="https://img.shields.io/github/last-commit/YOUR_USERNAME/YOUR_REPOSITORY" alt="GitHub last commit"></a>
</p>

# DB Reborn

### Uma ferramenta para converter JSON do DragonBones (v3.3) para JSON do Spine, para uso na Game Engine Defold.

## Introdução

O DB Reborn é uma ferramenta gratuita e de código aberto que converte animações do clássico editor DragonBones para o formato moderno Spine JSON. Isso permite que você use suas animações do DragonBones em uma vasta gama de game engines e frameworks populares.

Embora tenha sido criado originalmente para a **Game Engine Defold**, o DB Reborn é uma ponte universal para qualquer desenvolvedor que busca um fluxo de trabalho gratuito para animação de recorte. Ao gerar um arquivo Spine JSON padrão, ele torna suas animações compatíveis com engines como **Godot, Unity, GameMaker** e muitas outras.

**Para quem é esta ferramenta?**
*   **DB Reborn é ideal para:** Hobbistas e desenvolvedores independentes que buscam uma forma gratuita de criar e usar animações de recorte na sua game engine de preferência.
*   **Para trabalho profissional:** Se você precisa de recursos avançados e suporte dedicado, recomendamos fortemente a compra de uma [licença do Spine](http://esotericsoftware.com/ ).

## Compatibilidade com Engines

O DB Reborn gera um arquivo Spine JSON padrão, tornando-o compatível com praticamente qualquer game engine que possua um runtime para Spine. O novo seletor de saída permite que você escolha a extensão de arquivo correta para a sua engine.

*   **`.json` (Padrão):** Para **Godot, Unity, GameMaker, Phaser, Cocos2d-x, LibGDX** e a maioria das outras engines.
*   **`.spinejson` (Específico):** A extensão convencional para a **Game Engine Defold**.

Se sua engine ou framework suporta Spine JSON, ele funcionará com o DB Reborn.

## **AVISO IMPORTANTE**

Este projeto é uma ferramenta de conversão de formato de arquivo e não possui afiliação com a Esoteric Software. O propósito de gerar arquivos no formato JSON do Spine é permitir a interoperabilidade. Lembre-se que para utilizar as animações exportadas em seu jogo com as Runtimes oficiais do Spine, você e/ou sua empresa podem precisar adquirir uma licença apropriada do Spine, de acordo com os termos de serviço da Esoteric Software.

## Como Usar

### 1. Crie sua Animação

- Crie sua animação no **DragonBones 5.6.2**.
- **Requisitos:** Seu projeto deve conter no mínimo 1 armadura (*armature*), 1 osso (*bone*), 1 *slot* com 1 *skin* e 1 animação.

### 2. Exporte do DragonBones

- Exporte seu projeto com **Data Type: `JSON`** e **Data Version: `3.3`**.
- Garanta que as imagens sejam exportadas com **escala de 100%**.
- **Importante:** Não use *texture atlases* na exportação. A ferramenta requer *sprites* `.png` individuais.
- Após exportar, você terá um arquivo `SEU_ARQUIVO.json` e uma pasta `SEU_ARQUIVO_TEXTURES`.

### 3. Execute o DB Reborn

Você tem duas opções para rodar a aplicação:

**Opção A: Baixar o Aplicativo (Modo Fácil)**

1. Vá para a [página de Releases](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/releases) no GitHub.
2. Baixe o executável para Windows ou Linux.
3. Execute o aplicativo.

**Opção B: Executar a partir do Código-Fonte (para usuários macOS ou usuários avançados)**

1. Baixe a pasta `Source`.

2. Tenha o Python 3 instalado em seu sistema.

3. Instale os módulos necessários executando:
   
   Bash
   
   ```
   pip install PySide6 Pillow
   ```

4. Você pode então rodar a interface gráfica ou usar a linha de comando.

**Usando a Interface de Linha de Comando (CLI):** Abra seu terminal dentro da pasta `Source` e execute o script com os seguintes argumentos:

Bash

```
python3 db_reborn.py "caminho/para/seu.json" "caminho/para/pasta_de_saida" "4.2.22" "tipo_de_ease"
```

- `"caminho/para/seu.json"`: O caminho completo para o arquivo JSON de entrada do DragonBones.
- `"caminho/para/pasta_de_saida"`: A pasta onde o arquivo `.spinejson` será salvo.
- `"4.2.22"`: A versão alvo do Spine (atualmente fixa).
- `"tipo_de_ease"`: Use `"curve"` para converter as curvas de suavização ou `"linear"` para forçar transições lineares.

### 4. Converta o Arquivo

1. Abra o DB Reborn.
   
   ![DB Reborn Main Window](images/1_db_reborn_window.png)

2. Clique no botão "..." para selecionar seu arquivo de entrada `.json` 3.3 gerado do Dragonbones.
   
   *Observação: Após selecionar o  `.json`, o DB Reborn fará verificações no arquivo para ver se ele está de acordo com o padrão para ser convertido corretamente. Três janelas popup irão aparecer em sequência: Uma indicando que o  `.json` está aparentemente OK, outra que foi localizada a pasta  `SEU_ARQUIVO_TEXTURES` e a última, que a pasta contém as imagens do projeto. É só clicar no botão de OK em cada "popup" para prosseguir.*

3. O próximo passo é clicar no segundo botão "..." para selecionar a pasta de saída e o arquivo de saída. Escolha a extensão para o arquivo (`.json` ou `.spinejson`).
    ![DB Reborn Texture Folder](images/2_db_reborn_window_copy_texture_folder.png)
   
   *Observação: Caso você selecione uma pasta de saída diferente da pasta onde está localizado o `.json`, o DB Reborn irá tornar a checkbox 'Copy Texture Folder' ativa, fornecendo a opção de copiar a pasta `SEU_ARQUIVO_TEXTURES` para o novo local. É só marcar o "checkbox". Caso deseje apenas gerar o `.json` ou `.spinejson`, deixe o "checkbox" desmarcado.*

4. Clique em **Converter!**

![DB Reborn Success](images/3_db_reborn_window_success.png)

### 5. Importe na Defold

1. Copie o arquivo `SEU_ARQUIVO.spinejson` gerado e a pasta `SEU_ARQUIVO_TEXTURES` para o seu projeto Defold.
2. No seu arquivo `game.project`, adicione a [dependência da extensão do Spine](https://defold.com/manuals/spine/).
3. Crie um novo **Atlas** na Defold e adicione todas as imagens da pasta `SEU_ARQUIVO_TEXTURES`.
4. Crie uma nova **Spine Scene** (`.spinescene`) e associe seu arquivo `.spinejson` e o Atlas que você acabou de criar.
5. Adicione um componente **Spine Model** a um Game Object e selecione a nova Spine Scene.
6. Use um script para tocar sua animação, por exemplo: `spine.play("#spinemodel", "nome_da_sua_animacao")`.

## Problemas Conhecidos e Limitações

- **Curvas de Suavização (Easing):** O script tenta converter as curvas de *easing*. Se sua animação causar um erro fatal (*crash*) na Defold, tente reconverter marcando a caixa **"Force Linear"**. Isso mudará todas as transições para lineares.
  
  ![DB Reborn Success](images/4_force_linear.png)

- **Propriedades de Cisalhamento (Shear):** O DragonBones gera automaticamente *keyframes* de "shear" em seu JSON, mesmo sem uma interface para controlá-los. Para prevenir problemas no script, o DB Reborn remove todas as *curvas* de "shear", deixando apenas os *keyframes* de tempo, que não afetam a animação final.
  
  ![DB Reborn Success](images/5_dragonbones_properties.png)

## Suporte e Contribuição

- Para tutoriais e novidades, visite o [Canal no YouTube](https://www.youtube.com/@rfmcodedev).
- Por favor, reporte qualquer bug enviando um e-mail para [rfm.code.dev@gmail.com](mailto:rfm.code.dev@gmail.com).

## ❤️ Faça uma doação ao Projeto

Se este projeto te ajudou, considere me pagar um café! Cada pequena contribuição me ajuda a dedicar mais tempo ao desenvolvimento de software de código aberto.

<p align="center">
  <a href="https://ko-fi.com/SEU_USUARIO_KOFI" target="_blank"><img src="https://cdn.ko-fi.com/cdn/kofi3.png?v=3" alt="Buy Me a Coffee at ko-fi.com" height="40"></a>
</p>

Divirta-se!

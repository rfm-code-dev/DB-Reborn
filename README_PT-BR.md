[Read this in English](README.md)

<p align="center">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/python-3.7%2B-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://github.com/rfm-code-dev/DB-Reborn/releases/"><img src="https://img.shields.io/github/downloads/rfm-code-dev/DB-Reborn/total?cache=1" alt="GitHub all releases"></a>
  <a href="https://github.com/rfm-code-dev/DB-Reborn/commits/main"><img src="https://img.shields.io/github/last-commit/rfm-code-dev/DB-Reborn?cache=1" alt="GitHub last commit"></a>
  <a href="https://github.com/rfm-code-dev/DB-Reborn/blob/main/LICENSE.txt"><img src="https://img.shields.io/badge/license-EULA%20Freeware-blue" alt="License"></a>
</p>

# DB Reborn

### Uma ferramenta para converter JSON do DragonBones (v3.3) para JSON do Spine para uso em animações em jogos.

## Introdução

O DB Reborn é uma ferramenta gratuita que converte animações do clássico editor DragonBones para o formato moderno Spine JSON. Isso permite que você use suas animações do DragonBones em uma vasta gama de game engines e frameworks populares.

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
💥 Você pode encontrar um modelo de projeto na pasta example/ para testar imediatamente o processo de conversão 💥

### 1. Crie sua Animação

- Crie sua animação no **DragonBones 5.6.2**.
- **Requisitos:** Seu projeto deve conter no mínimo 1 armadura (*armature*), 1 osso (*bone*), 1 *slot* com 1 *skin* e 1 animação.

### 2. Exporte do DragonBones

- Exporte seu projeto com **Data Type: `JSON`** e **Data Version: `3.3`**.
- Garanta que as imagens sejam exportadas com **escala de 100%**.
- **Importante:** Não use *texture atlases* na exportação. A ferramenta requer *sprites* `.png` individuais.
- Após exportar, você terá um arquivo `SEU_ARQUIVO.json` e uma pasta `SEU_ARQUIVO_TEXTURES`.

### 3. Execute o DB Reborn

1. Vá para a [página de Releases](https://github.com/rfm-code-dev/DB-Reborn/releases) no GitHub.
2. Baixe o executável para Windows, Mac ou Linux.
3. Execute o aplicativo.

   *Nota para usuários de MacOS: Na primeira vez que você abrir o DB Reborn a inicialização pode levar até um minuto. Isso ocorre porque o macOS está verificando a segurança do aplicativo. As aberturas seguintes serão muito mais rápidas. Caso o aplicativo não abra, clique com o botão direito sobre ele e selecione Abrir.*

   *Compatibilidade com Apple Silicon (M1, M2, M3): Este aplicativo foi compilado para Macs baseados em Intel. Em Macs com processadores Apple Silicon, ele funciona perfeitamente através do Rosetta 2. Caso você não tenha o Rosetta instalado, o macOS perguntará automaticamente se deseja instalá-lo ao abrir o aplicativo pela primeira vez.*
   
   ![DB Reborn Main Window](images/1_db_reborn_window.png)

5. Clique no botão "..." para selecionar seu arquivo de entrada `.json` 3.3 gerado do Dragonbones.
   
   *Observação: Após selecionar o  `.json`, o DB Reborn fará verificações no arquivo para ver se ele está de acordo com o padrão para ser convertido corretamente. Três janelas popup irão aparecer em sequência: Uma indicando que o  `.json` está aparentemente OK, outra que foi localizada a pasta  `SEU_ARQUIVO_TEXTURES` e a última, que a pasta contém as imagens do projeto. É só clicar no botão de OK em cada "popup" para prosseguir.*

6. O próximo passo é clicar no segundo botão "..." para selecionar a pasta de saída e o arquivo de saída. Escolha a extensão para o arquivo (`.json` ou `.spinejson`).

    ![DB Reborn Texture Folder](images/2_db_reborn_window_copy_texture_folder.png)
   
   *Observação: Caso você selecione uma pasta de saída diferente da pasta onde está localizado o `.json`, o DB Reborn irá tornar a checkbox 'Copy Texture Folder' ativa, fornecendo a opção de copiar a pasta `SEU_ARQUIVO_TEXTURES` para o novo local. É só marcar o "checkbox". Caso deseje apenas gerar o `.json` ou `.spinejson`, deixe o "checkbox" desmarcado.*

7. Clique em **Converter!**

    ![DB Reborn Success](images/3_db_reborn_window_success.png)

### 4. Importe na Defold Game Engine

1. Copie o arquivo `SEU_ARQUIVO.spinejson` gerado e a pasta `SEU_ARQUIVO_TEXTURES` para o seu projeto Defold.
2. No seu arquivo `game.project`, adicione a [dependência da extensão do Spine](https://defold.com/manuals/spine/).
3. Crie um novo **Atlas** na Defold e adicione todas as imagens da pasta `SEU_ARQUIVO_TEXTURES`.
4. Crie uma nova **Spine Scene** (`.spinescene`) e associe seu arquivo `.spinejson` e o Atlas que você acabou de criar.
5. Adicione um componente **Spine Model** a um Game Object e selecione a nova Spine Scene.
6. Use um script para tocar sua animação, por exemplo: `spine.play("#spinemodel", "nome_da_sua_animacao")`.

## Problemas Conhecidos e Limitações

- **Curvas de Suavização (Easing) #1:** O script tenta converter as curvas de *easing*. Se sua animação causar um erro fatal (*crash*) na Defold, tente reconverter marcando a caixa **"Force Linear"**. Isso mudará todas as transições para lineares.
  
  ![DB Reborn Success](images/4_force_linear.png)

- **Curvas de Suavização (Easing) #2:** Como o DB Reborn converte automaticamente todos os quadros-chave com curvas de suavização, se você usar curvas de suavização em todos os quadros-chave, todos serão convertidos. Isso pode resultar em movimentos indesejados, especialmente se houver dois quadros-chave iguais e você não quiser que haja movimento entre eles. Portanto, recomendo que você defina o primeiro quadro-chave como linear para evitar esse problema.
  
  ![Dragonbones Linear](images/6_ease_curve_linear.png)

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

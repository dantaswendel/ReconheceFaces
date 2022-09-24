<h1 align="center" id="topo">Reconhecimento de Faces</h1>

- [X] Esse programa  faz o reconhecimento de faces  de imagens em presentes em um Bucket S3 (AWS), usando o Amazon Rekognition e a linguagem Python.
- [X] O resultado da comparação é exibido em um site estático que tambem está hospedado em um Bucket na AWS.
- [X] Esse programa deve ser ativado através de uma função Lambda que tem como gatailho (trigger) o fato de uma nova imagem com o nome especificado ser adicionada ao Bucket de imagens.
- [X] O Programa pode ser acionado localmente sem a necessidade de uma Função Lambda


<h3 id="Métodos">Métodos</h3>
Os métodos do programa e o que cada um faz:

<h4 id="Index">Index</h4>

- Lista as imagens presentes no Bucket.

```
def lista_imagens():
    imagens =[]
    bucket = s3.Bucket('faimagem')
    for imagem in bucket.objects.all():
        imagens.append(imagem.key)
        print(imagens)
    return imagens
```

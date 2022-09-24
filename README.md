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
- Indexa imagens na coleção.

```
def indexa_colecao(imagens):
    for i in imagens:
        response=client.index_faces(
            CollectionId='faces',
            DetectionAttributes=[
            ],
            ExternalImageId=i[:-4],
            Image={
                'S3Object':{
                    'Bucket': 'faimagem',
                    'Name': i,
                },
            },
        )
```

<h4 id="analiseFaces">analiseFaces</h4>

- Detecta faces nas imagens.

```
def detecta_faces():
    faces_detectadas = client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARIA',
        Image={
            'S3Object': {
                'Bucket': 'faimagem',
                'Name': '_ANALISE.png',
            },
        },
    )
     return faces_detectadas
```

- Cria uma lista com as faces detectadas nas imagens.

```
def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for imagens in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagens]['Face']['FaceId'])
    return faceId_detectadas

```

- Compara as imagens e reconhece as faces presentes no bucket em relação a nova imagem de parametro para a comparação.

```
def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for ids in faceId_detectadas:
        resultado_comparacao.append(
            client.search_faces(
                CollectionId='faces',
                FaceId=ids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado_comparacao


```


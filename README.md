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

- Transforma os dados da comparação em um JSon, com as informações de Nome, e a a porcentagem de semelhança das faces 

```
def gera_dados_json(resultado_comparacao):
    dados_json = []
    for face_matches in resultado_comparacao:
        if(len(face_matches.get('FaceMatches'))) >=1:
            perfil = dict(nome=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                          faceMatch=round(face_matches['FaceMatches'][0]['Similarity'], ))
            dados_json.append(perfil)
    return dados_json

```
- Publica os dados Json no Site 

```
ddef publica_dados(dados_json):
    arquivo = s3.Object('fasite', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))
```

- Exclui a imagem de comparação do Bucket de imagens

```
def exclui_imagem_colecao(faceId_detectadas):
    client.delete_faces(
        CollectionId='faces',
        FaceIds=faceId_detectadas,
    )
```

- CHAMA TODOS OS OUTROS MÉTODOS

```
def main():
    faces_detectadas = detecta_faces()
    faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
    resultado_comparacao = compara_imagens(faceId_detectadas)
    dados_json = gera_dados_json(resultado_comparacao)
    publica_dados(dados_json)
    exclui_imagem_colecao(faceId_detectadas)
    print(json.dumps(dados_json, indent=4))
```

<h2 id="Tecnologias">Tecnologias utilizadas </h2>

<a href="https://aws.amazon.com/pt/lambda/">
        <img align="center" alt="AWS - Lambda" title="AWS - Lambda" height="80px" width="80px" src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Amazon_Lambda_architecture_logo.png"/>
    </a>
    <a href="https://aws.amazon.com/pt/s3/?trk=9c7f9c59-8d98-452d-8a14-441a9b6492f3&sc_channel=ps&s_kwcid=AL!4422!3!589951433465!e!!g!!amazon%20s3&ef_id=Cj0KCQjw1bqZBhDXARIsANTjCPK5w2A7CcqPN7DZJf11fk9kZcCgouSwJkoVKgauQMyeAlSB3mYlEBcaArycEALw_wcB:G:s&s_kwcid=AL!4422!3!589951433465!e!!g!!amazon%20s3">
        <img align="center" alt="Git" title="Git" height="80px" width="90px" src="https://connectoricons-prod.azureedge.net/releases/v1.0.1597/1.0.1597.3005/amazons3/icon.png"/>
    </a>
    <a href="https://www.python.org/">
        <img align="center" alt="PYTHON" title="PYTHON" height="80px" width="90px" src="https://cdn.icon-icons.com/icons2/112/PNG/512/python_18894.png"/>
    </a>
        <a href="https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html">
        <img align="center" alt="Rekognition" title="Rekognition" height="80px" width="90px" src="https://cdn.icon-icons.com/icons2/112/PNG/512/python_18894.png"/>
    </a>


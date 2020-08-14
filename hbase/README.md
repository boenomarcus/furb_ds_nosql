# hbase
Atividade Prática Hbase - Especialização Data Science FURB 


# Aquecendo com alguns dados 

### **Exercício 1 - Crie a tabela com 2 famílias de colunas: (a) personal-data (b) professional-data**

*1.1 - Crie a tabela com 2 famílias de colunas: (a) personal-data (b) professional-data*

**Queries:**

```shell
create 'italians', 'personal-data', 'professional-data'
```

**Retorno do HBase:**

```shell
Created table italians
Took 1.2616 seconds
=> Hbase::Table - italians
```

---

*1.2 - Importe o arquivo via linha de comando*

O seguinte comando foi executado no root do container contendo a imagem do hbase-furb 

```shell
hbase shell /tmp/italians.txt
```

**Checando inserção de dados:**

```shell
hbase(main):003:0> scan 'italians'
ROW                                                COLUMN+CELL
 1                                                 column=personal-data:city, timestamp=1588098892594, value=Verona
 1                                                 column=personal-data:name, timestamp=1588098892533, value=Paolo Sorrentino
 1                                                 column=professional-data:role, timestamp=1588098892606, value=Gestao Comercial
 1                                                 column=professional-data:salary, timestamp=1588098892617, value=2394
 10                                                column=personal-data:city, timestamp=1588098893229, value=Milan
 10                                                column=personal-data:name, timestamp=1588098893216, value=Giovanna Caputo
 10                                                column=professional-data:role, timestamp=1588098893261, value=Comunicacao Institucional
 10                                                column=professional-data:salary, timestamp=1588098893277, value=9470
 2                                                 column=personal-data:city, timestamp=1588098892647, value=Padua
 2                                                 column=personal-data:name, timestamp=1588098892632, value=Domenico Barbieri
 2                                                 column=professional-data:role, timestamp=1588098892664, value=Psicopedagogia
 2                                                 column=professional-data:salary, timestamp=1588098892681, value=11890
 3                                                 column=personal-data:city, timestamp=1588098892705, value=Taranto
 ...
```

---

### **Exercício 2 - Agora execute as seguintes operações**

*2.1 - Adicione mais 2 italianos mantendo adicionando informações como data de nascimento nas informações pessoais e um atributo de anos de experiência nas informações profissionais*

**Queries:**

```shell
put 'italians', '11', 'personal-data:name',  'Ezio Auditore'
put 'italians', '11', 'personal-data:city',  'Firenze'
put 'italians', '11', 'personal-data:born',  '1994-02-28'
put 'italians', '11', 'professional-data:role',  'Analista de Dados'
put 'italians', '11', 'professional-data:yearsOfExperience',  '2'
put 'italians', '11', 'professional-data:salary',  '3500'
put 'italians', '12', 'personal-data:name',  'Enzo Gorlomi'
put 'italians', '12', 'personal-data:city',  'Spormaggiore'
put 'italians', '12', 'personal-data:born',  '1985-07-12'
put 'italians', '12', 'professional-data:role',  'DevOps'
put 'italians', '12', 'professional-data:yearsOfExperience',  '15'
put 'italians', '12', 'professional-data:salary',  '7400'
```

**Checando inserção de dados:**

```shell
hbase(main):022:0> get 'italians', 11
COLUMN                                             CELL
 personal-data:born                                timestamp=1588100220337, value=1994-02-28
 personal-data:city                                timestamp=1588100212778, value=Firenze
 personal-data:name                                timestamp=1588100204904, value=Ezio Auditore
 professional-data:role                            timestamp=1588100226567, value=Analista de Dados
 professional-data:salary                          timestamp=1588100238704, value=3500
 professional-data:yearsOfExperience               timestamp=1588100232418, value=2
1 row(s)
Took 0.1175 seconds
hbase(main):023:0> get 'italians', 12
COLUMN                                             CELL
 personal-data:born                                timestamp=1588100254869, value=1985-07-12
 personal-data:city                                timestamp=1588100249697, value=Spormaggiore
 personal-data:name                                timestamp=1588100244681, value=Enzo Gorlomi
 professional-data:role                            timestamp=1588100259962, value=DevOps
 professional-data:salary                          timestamp=1588100271456, value=7400
 professional-data:yearsOfExperience               timestamp=1588100265830, value=15
1 row(s)
Took 0.0321 seconds
```

---

*2.2 - Adicione o controle de 5 versões na tabela de dados pessoais*

**Queries:**

```shell
alter 'italians', NAME=>'personal-data', VERSIONS=>5
```

**Retorno do HBase:**

```shell
hbase(main):025:0> alter 'italians', NAME=>'personal-data', VERSIONS=>5
Updating all regions with the new schema...
1/1 regions updated.
Done.
Took 2.3291 seconds
```

---

*2.3 - Faça 5 alterações em um dos italianos*

**Queries:**

```shell
put 'italians', '11', 'personal-data:city',  'FIRENZE'
put 'italians', '11', 'personal-data:city',  'Florence'
put 'italians', '11', 'personal-data:city',  'florence'
put 'italians', '11', 'personal-data:city',  'Florenca'
put 'italians', '11', 'personal-data:city',  'Firenze'
```

---

*2.4 - Com o operador get, verifique como o HBase armazenou o histórico*

**Queries:**

```shell
get 'italians', 11, COLUMN=>'personal-data:city', VERSIONS=>5
```

**Retorno do HBase:**

```shell
hbase(main):007:0> get 'italians', 11, COLUMN=>'personal-data:city', VERSIONS=>5
COLUMN                                             CELL
 personal-data:city                                timestamp=1588101515596, value=Firenze
 personal-data:city                                timestamp=1588101510081, value=Florenca
 personal-data:city                                timestamp=1588101474265, value=florence
 personal-data:city                                timestamp=1588101467518, value=Florence
 personal-data:city                                timestamp=1588101459714, value=FIRENZE
1 row(s)
Took 0.0842 seconds
```

---

*2.5 - Utilize o scan para mostrar apenas o nome e profissão dos italianos*

**Queries:**

```shell
scan 'italians', COLUMNS => ['personal-data:name', 'professional-data:role'] 
```

**Retorno do HBase:**

```shell
hbase(main):014:0> scan 'italians', COLUMNS => ['personal-data:name', 'professional-data:role']
ROW                                                COLUMN+CELL
 1                                                 column=personal-data:name, timestamp=1588098892533, value=Paolo Sorrentino
 1                                                 column=professional-data:role, timestamp=1588098892606, value=Gestao Comercial
 10                                                column=personal-data:name, timestamp=1588098893216, value=Giovanna Caputo
 10                                                column=professional-data:role, timestamp=1588098893261, value=Comunicacao Institucional
 11                                                column=personal-data:name, timestamp=1588100204904, value=Ezio Auditore
 11                                                column=professional-data:role, timestamp=1588101384717, value=Analista de Dados
 12                                                column=personal-data:name, timestamp=1588100244681, value=Enzo Gorlomi
 12                                                column=professional-data:role, timestamp=1588100259962, value=DevOps
 2                                                 column=personal-data:name, timestamp=1588098892632, value=Domenico Barbieri
 2                                                 column=professional-data:role, timestamp=1588098892664, value=Psicopedagogia
 3                                                 column=personal-data:name, timestamp=1588098892691, value=Maria Parisi
 3                                                 column=professional-data:role, timestamp=1588098892722, value=Optometria
 4                                                 column=personal-data:name, timestamp=1588098892745, value=Silvia Gallo
 4                                                 column=professional-data:role, timestamp=1588098892765, value=Engenharia Industrial Madeireira
 5                                                 column=personal-data:name, timestamp=1588098892798, value=Rosa Donati
 5                                                 column=professional-data:role, timestamp=1588098892838, value=Mecatronica Industrial
 6                                                 column=personal-data:name, timestamp=1588098892884, value=Simone Lombardo
 6                                                 column=professional-data:role, timestamp=1588098892938, value=Biotecnologia e Bioquimica
 7                                                 column=personal-data:name, timestamp=1588098892972, value=Barbara Ferretti
 7                                                 column=professional-data:role, timestamp=1588098893009, value=Libras
 8                                                 column=personal-data:name, timestamp=1588098893050, value=Simone Ferrara
 8                                                 column=professional-data:role, timestamp=1588098893087, value=Engenharia de Minas
 9                                                 column=personal-data:name, timestamp=1588098893126, value=Vincenzo Giordano
 9                                                 column=professional-data:role, timestamp=1588098893174, value=Marketing
12 row(s)
Took 0.1325 seconds
```
---

*2.6 - Apague os italianos com row id ímpar*

Neste caso mantive o italiano de row id 5 para evitar conflitos nos exercícios 2.7 e 2.8 (seguintes) 

**Queries:**

```shell
deleteall 'italians', '1'
deleteall 'italians', '3'
deleteall 'italians', '7'
deleteall 'italians', '9'
deleteall 'italians', '11'
```

---

*2.7 - Crie um contador de idade 55 para o italiano de row id 5*

**Queries:**

```shell
incr 'italians', '5', 'personal-data:age', 55
```
**Retorno do HBase:**

```shell
hbase(main):036:0> incr 'italians', '5', 'personal-data:age', 55
COUNTER VALUE = 55
Took 0.0387 seconds
```
---

*2.8 - Incremente a idade do italiano em 1*

**Queries:**

```shell
incr 'italians', '5', 'personal-data:age', 1
```

**Retorno do HBase:**

```shell
hbase(main):039:0> incr 'italians', '5', 'personal-data:age', 1
COUNTER VALUE = 56
Took 0.0155 seconds
```

---

# Exercício 3 - Os italianos voltaram!

*Alteração script JS para popular base de dados*

Abra um terminal/CMD e navegue até a pasta que contém os arquivos deste repositorio. Em seguida execute o seguinte comando para rodar o script JS pelo node.js

```shell
node italian-people_modified.js > italians_hbase.txt
```

O resultado será salvo em um arquivo txt contendo os comandos HBase Shell para criar e popular uma nova tabela com o nome `italians`. 

Em seguida transfira o arquivo txt para o container hbase-furb com o seguinte comando:

```shell
docker cp .\italians_hbase.txt hbase-furb:/tmp
```
Dê start no container hbase-furb e abra o seu respectivo shell. Caso exista uma tabela com o nome `italians` no HBase se faz necessário deletá-la por meio dos seguintes comandos:

```shell
hbase shell disable 'italians'
hbase shell drop 'italians'
```

Agora estamos prontos para criar e popular nossa nova tabela. Para tanto, execute o seguinte comando no shell do container:

```shell
hbase shell /tmp/italians_hbase.txt
```

---
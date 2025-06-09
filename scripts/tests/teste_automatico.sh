#!/bin/bash

# Teste automático com transcrições densas

OPEN_RESULTS=${1:-"no"}  # Por padrão não abre


echo "🧹 Limpando projetos de teste anteriores..."
rm -rf projects/teste_auto_*

echo "🗑️ Limpando comparações de teste..."
# Debug - ver o que está sendo removido
echo "  Arquivos a remover:"
ls -la projects/comparisons/*_test* 2>/dev/null || echo "  Nenhum arquivo *_test encontrado"
rm -rf projects/comparisons/*_test*

source transcript_env/bin/activate

# Você pode mudar estes nomes!
PROJ1="teste_auto_individual"
PROJ2="teste_auto_dupla"
PROJ3="teste_auto_trio"

echo "🚀 Criando projetos..."
python run_analysis.py --create-project $PROJ1
python run_analysis.py --create-project $PROJ2
python run_analysis.py --create-project $PROJ3

echo "📝 Gerando transcrições automáticas densas..."

# PROJETO 1 - Uma transcrição densa
cat > projects/$PROJ1/arquivos/entrevista_completa.txt << 'EOF'
Entrevistador: Gostaria que você compartilhasse sua experiência com a implementação de tecnologias educacionais em sua instituição.

Participante: Olha, é uma questão bem complexa, né? Eu trabalho há 15 anos na educação e vi muitas mudanças. No começo, a gente tinha aquela resistência natural, sabe? Tipo, "ah, sempre funcionou assim, por que mudar?". Mas aí a pandemia veio e meio que forçou todo mundo a se adaptar.

Entrevistador: E como foi esse processo de adaptação?

Participante: Foi... como posso dizer... foi caótico no início. A gente não tinha infraestrutura, os professores não sabiam usar as ferramentas, os alunos não tinham equipamento em casa. Foi um desafio enorme. Mas sabe o que mais me impressionou? A capacidade de adaptação de todo mundo. Em questão de meses, professores que mal sabiam ligar um computador estavam dando aulas online, criando conteúdo digital.

Mas assim, não foi só aprender a usar a tecnologia, entende? Foi repensar toda a metodologia. Porque não adianta pegar uma aula tradicional e simplesmente colocar na frente de uma câmera. Não funciona. Os alunos dispersam, não prestam atenção. Então a gente teve que aprender a criar conteúdo interativo, usar ferramentas de engajamento, repensar a avaliação.

Entrevistador: Quais foram os principais desafios que vocês enfrentaram?

Participante: Ah, foram muitos... Primeiro, a questão da infraestrutura mesmo. Internet de qualidade, equipamentos adequados, tanto para professores quanto para alunos. Tivemos que fazer campanhas de arrecadação de notebooks, tablets. Foi uma mobilização da comunidade toda.

Depois, a questão pedagógica. Como manter a qualidade do ensino? Como avaliar de forma justa? Como identificar se o aluno está realmente aprendendo ou só copiando e colando? Essas questões ainda não estão totalmente resolvidas, para ser honesta.

E tem a questão humana também, né? O isolamento, a falta de contato. Educação não é só transmissão de conteúdo, é formação humana, é socialização. Como fazer isso através de uma tela? Alguns alunos se adaptaram bem, outros sofreram muito. Tivemos casos de depressão, ansiedade. Foi bem difícil.

Entrevistador: E hoje, com o retorno presencial, como vocês estão lidando com o uso da tecnologia?

Participante: Então, essa é a parte interessante. A gente descobriu que algumas coisas funcionam melhor online. Por exemplo, aulas de reforço, plantões de dúvidas, alguns tipos de avaliação. Então estamos num modelo híbrido agora. 

Mas é um híbrido pensado, sabe? Não é simplesmente "ah, vamos usar tecnologia porque é moderno". É usar onde faz sentido, onde agrega valor. Por exemplo, nas aulas de matemática, os professores usam aplicativos que permitem visualizar gráficos em 3D, fazer simulações. Isso é incrível, não tinha como fazer isso no quadro negro.

Por outro lado, nas discussões de literatura, nada substitui o debate presencial, a troca de olhares, a construção coletiva do conhecimento. Então é esse equilíbrio que a gente busca.

Entrevistador: E qual sua visão para o futuro?

Participante: Eu sou otimista, mas com os pés no chão. Acho que a tecnologia veio para ficar e pode ser uma aliada poderosa na educação. Mas não podemos perder de vista o essencial: o ser humano. A tecnologia é ferramenta, o professor continua sendo fundamental, a interação humana é insubstituível.

O que eu espero é que a gente consiga usar o melhor dos dois mundos. Usar a tecnologia para personalizar o ensino, para atender as necessidades individuais de cada aluno, para democratizar o acesso ao conhecimento. Mas sem perder a humanidade, a empatia, o cuidado com o outro.

É um caminho longo ainda, temos muito a aprender, muitos erros pela frente também. Mas eu acredito que estamos na direção certa. O importante é não ter medo de experimentar, de errar, de recomeçar. Educação é isso, né? É um processo constante de aprendizagem, tanto para os alunos quanto para nós, educadores.
EOF

# PROJETO 2 - Primeira transcrição
cat > projects/$PROJ2/arquivos/professor_matematica.txt << 'EOF'
Entrevistador: Como professor de matemática, como você vê a integração de tecnologia em suas aulas?

Professor: Cara, mudou completamente minha forma de ensinar. Sério mesmo. Eu era daqueles professores tradicionais, sabe? Quadro, giz, lista de exercícios. E funcionava, mas eu sempre sentia que faltava algo, especialmente com os alunos que tinham mais dificuldade.

A tecnologia me abriu possibilidades que eu nem imaginava. Por exemplo, geometria espacial. Antes eu ficava desenhando no quadro, tentando representar figuras 3D em 2D, e os alunos ficavam boiando. Hoje eu uso o GeoGebra, eles podem rotacionar as figuras, ver de todos os ângulos, entender de verdade o que é um cone, uma esfera seccionada.

Mas não é só isso. O que mais me impressiona é a possibilidade de personalização. Eu uso plataformas que me mostram exatamente onde cada aluno está com dificuldade. Tipo, o João não entende frações, a Maria tem problema com equações de segundo grau. Antes eu só descobria isso na prova, quando já era tarde demais.

Entrevistador: E os desafios?

Professor: Ah, tem muitos. Primeiro, nem todos os alunos têm acesso igual à tecnologia. Isso cria uma disparidade que me preocupa muito. A gente tenta contornar, empresta equipamento, mas não é ideal.

Depois, tem a questão da distração. Celular em sala de aula é uma faca de dois gumes. Pode ser uma ferramenta incrível ou uma fonte infinita de distração. WhatsApp, Instagram, jogos... é uma batalha constante.

E tem a minha própria limitação também. Eu não sou nativo digital, tive que aprender muita coisa. Às vezes os alunos sabem mais de tecnologia que eu, o que é humilhante mas também uma oportunidade de aprender com eles.

O maior desafio, na minha opinião, é não deixar a tecnologia substituir o raciocínio. É muito fácil o aluno jogar a equação no Photomath e pegar a resposta. Mas ele aprendeu? Desenvolveu o raciocínio lógico? Essas são questões que me tiram o sono.

Entrevistador: Como você equilibra isso?

Professor: Tento usar a tecnologia como apoio, não como muleta. Por exemplo, depois que eles entendem o conceito, aí sim usamos calculadoras gráficas, aplicativos. A tecnologia vem para expandir, não para substituir o pensamento.

E eu aprendi a usar a própria tecnologia para combater o uso inadequado. Faço atividades que exigem explicação do raciocínio, não só a resposta. Uso ferramentas colaborativas onde eles têm que trabalhar juntos. É um processo de constante adaptação.

No final, eu acho que vale a pena. Vejo alunos que odiavam matemática descobrindo que podem gostar, podem entender. Isso não tem preço. A tecnologia, quando bem usada, democratiza o aprendizado, torna a matemática mais acessível, menos assustadora. E esse é o meu objetivo como professor.
EOF

# PROJETO 2 - Segunda transcrição
cat > projects/$PROJ2/arquivos/coordenadora_pedagogica.txt << 'EOF'
Entrevistador: Como coordenadora pedagógica, qual sua perspectiva sobre a implementação de tecnologias educacionais?

Coordenadora: É uma perspectiva bem ampla, porque eu vejo todos os lados, né? Vejo os professores lutando para se adaptar, os alunos às vezes mais perdidos do que ajudados, os pais preocupados, a direção pressionando por resultados. É um ecossistema complexo.

O que mais me marca é a desigualdade que a tecnologia pode amplificar. A gente fala muito de inclusão digital, mas na prática, o que vejo são alunos com notebooks de última geração e alunos compartilhando o celular da mãe para assistir aula. Como equalizar isso? É um desafio diário.

Entrevistador: E como vocês têm lidado com essa questão?

Coordenadora: Olha, a gente faz o que pode. Campanhas de arrecadação, parcerias com empresas, uso dos laboratórios da escola em horários estendidos. Mas é paliativo, sabe? O problema é estrutural, é de política pública.

O que tenta fazer é capacitar muito bem nossos professores. Porque um professor bem preparado consegue fazer maravilhas mesmo com recursos limitados. Temos formações constantes, grupos de estudo, compartilhamento de práticas. 

Uma coisa que funcionou bem foi criar uma mentoria entre professores. Os mais familiarizados com tecnologia ajudam os outros. Isso criou uma cultura colaborativa linda de ver. Professor de história aprendendo Excel com o de matemática, professora de português ensinando sobre blogs para o de geografia.

Entrevistador: Quais mudanças pedagógicas você observou?

Coordenadora: Muitas! A mais significativa é a mudança do professor como detentor único do conhecimento para um facilitador da aprendizagem. Com a internet, o aluno tem acesso a todo conhecimento do mundo. O papel do professor mudou, e isso assusta muita gente.

Vi professores brilhantes entrarem em crise porque achavam que não eram mais necessários. Tive que trabalhar muito essa questão emocional. Mostrar que eles são mais necessários do que nunca, mas de forma diferente. Não é mais sobre transmitir informação, é sobre ensinar a pensar, a filtrar, a questionar, a conectar conhecimentos.

A avaliação também mudou muito. Prova tradicional faz cada vez menos sentido num mundo onde a informação está a um clique. Estamos experimentando com projetos, portfolios, avaliação por competências. É um processo, tem resistência, tem erro, mas também tem muito aprendizado.

E a relação com as famílias mudou completamente. Antes os pais só apareciam em reunião bimestral. Agora eles têm acesso em tempo real ao que acontece na escola, podem ver as tarefas, as notas, conversar com professores. Isso é bom mas também cria novos desafios. Pais que querem controlar demais, que questionam toda decisão pedagógica.

Entrevistador: Qual sua visão para os próximos anos?

Coordenadora: Eu acho que estamos só no começo. Inteligência artificial, realidade virtual, personalização extrema do ensino... as possibilidades são infinitas. Mas minha preocupação é que a gente não perca o foco no que realmente importa: formar seres humanos completos.

Tecnologia é meio, não fim. Se ela nos ajuda a ter uma educação mais inclusiva, mais personalizada, mais engajante, ótimo. Mas se ela nos afasta, se cria mais barreiras, se desumaniza o processo educacional, então estamos no caminho errado.

Meu trabalho como coordenadora é garantir esse equilíbrio. É desafiador, é cansativo às vezes, mas é também extremamente gratificante. Cada pequena vitória, cada professor que supera o medo da tecnologia, cada aluno que descobre uma nova forma de aprender, isso me motiva a continuar.
EOF

# PROJETO 3 - Primeira transcrição
cat > projects/$PROJ3/arquivos/aluno_ensino_medio.txt << 'EOF'
Entrevistador: Como estudante, como você vê o uso de tecnologia na sua educação?

Aluno: Cara, pra mim é natural, sabe? Tipo, eu não consigo imaginar estudar sem internet, sem YouTube, sem os apps. Meus pais contam que eles tinham que ir na biblioteca, procurar em enciclopédia... parece idade da pedra pra mim.

Mas assim, não é essa maravilha toda que os adultos pensam. Tem muito professor que não sabe usar direito, aí fica pior que aula normal. Já tive professor que só pegava PowerPoint pronto da internet e lia slide. Pelo amor de Deus, né? Isso eu faço em casa.

O que funciona mesmo é quando o professor sabe integrar. Tipo, meu professor de biologia usa realidade aumentada pra mostrar o corpo humano. É muito louco, você vê o coração batendo, pode dar zoom nas células. Isso sim ajuda a entender.

Entrevistador: E quais são as dificuldades?

Aluno: Ah, tem várias. Primeiro, distração. Eu confesso, é muito difícil resistir. Tá ali o WhatsApp piscando, o Instagram chamando... A gente tenta focar, mas é difícil. Eu uso uns apps que bloqueiam outros apps, mas mesmo assim...

Outra coisa é o cansaço. Ficar o dia todo olhando pra tela cansa demais. Na pandemia era pior, tinha dia que eu terminava as aulas com dor de cabeça, vista embaçada. Presencial cansa também, mas é diferente.

E tem a pressão de estar sempre conectado. Professor manda tarefa às 10 da noite, espera resposta no domingo. Não tem mais separação entre escola e casa. Isso estressa.

Entrevistador: O que você acha que poderia melhorar?

Aluno: Primeiro, formar melhor os professores. Não adianta dar tablet pra todo mundo se o professor não sabe usar. E não é só saber mexer, é saber usar pedagogicamente, sabe? Fazer a tecnologia ajudar no aprendizado, não só complicar.

Segundo, entender que nem tudo precisa ser digital. Às vezes escrever no papel ajuda a fixar melhor. Às vezes uma discussão presencial é mais rica que um fórum online. Tem que ter equilíbrio.

E parar com essa neura de inovação por inovação. Nem toda aula precisa ser super tecnológica. Às vezes o professor falando e a gente discutindo é o que funciona. Tecnologia tem que vir pra somar, não pra substituir tudo.

Ah, e uma coisa importante: considerar a saúde mental. Esse excesso de tela, de estímulo, de informação, tá adoecendo muita gente. Ansiedade, depressão, déficit de atenção... é uma epidemia na minha geração. A escola precisa pensar nisso também.

Entrevistador: E o que você leva de positivo?

Aluno: Muita coisa! O acesso à informação é incrível. Posso aprender qualquer coisa, a qualquer hora. Se não entendi na aula, vejo videoaula. Se quero aprofundar, tem curso online. É democratizante, sabe?

E as possibilidades criativas são infinitas. Já fiz trabalho em vídeo, podcast, site, game... Isso desenvolve habilidades que vão ser úteis pra vida, não só pra escola.

A conexão com o mundo também. Já fiz projeto com alunos da Índia, participei de palestra com cientista da NASA, pratiquei inglês com gente do mundo todo. Isso não existia antes.

No final, acho que minha geração tá no meio dessa transição. A gente é cobaia, em certo sentido. Mas também somos protagonistas. Temos voz pra dizer o que funciona e o que não funciona. E eu sou otimista. Acho que dá pra construir uma educação que use o melhor da tecnologia sem perder o humano.
EOF

# PROJETO 3 - Segunda transcrição  
cat > projects/$PROJ3/arquivos/mae_de_aluno.txt << 'EOF'
Entrevistador: Como mãe, qual sua visão sobre o uso de tecnologia na educação do seu filho?

Mãe: Olha, é uma mistura de sentimentos, viu? Por um lado, eu vejo as oportunidades incríveis que meu filho tem. Coisas que eu nem sonhava na idade dele. Por outro, tenho muitas preocupações.

A pandemia foi um divisor de águas pra mim. Antes eu achava que era só dar um tablet e pronto, tá estudando. Mas quando vi de perto, nossa... é muito mais complexo. Vi meu filho lutando pra se concentrar, vi a dificuldade dos professores, vi a desigualdade gritante entre as famílias.

Entrevistador: Pode falar mais sobre essas preocupações?

Mãe: A principal é o tempo de tela. Meu filho fica horas no computador pra escola, depois quer relaxar... como? No videogame, no celular. É tela o dia todo. Isso não pode ser saudável. Já levei no oftalmologista, já está com problema de vista. E a postura? Uma katástrofe.

Tem a questão da segurança online também. Cyberbullying, conteúdo inadequado, predadores online... é um mundo que eu não domino completamente. Tento monitorar, conversar, mas sei que não consigo controlar tudo. É angustiante.

E o desenvolvimento social me preocupa muito. Essa geração sabe se comunicar por mensagem, mas na hora de falar pessoalmente, travam. Meu filho prefere mandar áudio do que ligar. Fazer trabalho em grupo pelo Meet ao invés de se encontrar. Que adultos eles vão ser?

Entrevistador: E os pontos positivos?

Mãe: Ah, tem muitos também! O acesso ao conhecimento é maravilhoso. Meu filho tira dúvidas no YouTube, aprende coisas que nem estão no currículo. Outro dia ele me explicou sobre buracos negros, aprendeu vendo vídeo de um astrofísico. Isso é incrível!

A comunicação com a escola melhorou muito. Tenho acesso às notas em tempo real, posso conversar com os professores, acompanhar as tarefas. Antes era uma caixa preta, agora é transparente. Isso ajuda muito no acompanhamento.

E vi meu filho desenvolver habilidades que eu não tenho. Ele edita vídeo, cria apresentações lindas, pesquisa com uma facilidade... São competências importantes pro futuro dele.

Entrevistador: Como você tenta equilibrar?

Mãe: É um desafio diário. Estabeleci regras: tempo de tela limitado, pausas obrigatórias, atividades offline. Mas confesso que é difícil manter. Às vezes cedo porque vejo que ele precisa pra escola, às vezes sou rígida demais e gera conflito.

Tento me informar, participo de grupos de pais, leio sobre o assunto. Mas a tecnologia evolui tão rápido que quando você acha que entendeu, mudou tudo de novo. É cansativo.

O que funciona melhor é o diálogo. Converso muito com meu filho, tento entender o mundo dele, mostro minhas preocupações sem demonizar a tecnologia. Não é fácil, ele acha que sou das cavernas às vezes, mas aos poucos a gente se entende.

E busco parcerias. Com a escola, com outros pais, com profissionais. Sozinha eu não dou conta. É preciso uma rede de apoio pra navegar nesse mundo novo.

Entrevistador: Que conselho daria para outros pais?

Mãe: Primeiro, não tenham medo de não saber. Ninguém tem todas as respostas. Estamos todos aprendendo juntos. Sejam curiosos, perguntem pros filhos, aprendam com eles.

Segundo, não demonizem a tecnologia. Ela veio pra ficar e tem muitos benefícios. O segredo é o equilíbrio, é o uso consciente. 

Terceiro, mantenham o diálogo aberto. Proibir não funciona, eles vão fazer escondido. Melhor é conversar, estabelecer regras juntos, entender as necessidades deles.

E cuidem de vocês também. É fácil se perder nessa vigilância constante, nessa preocupação. Mas pais estressados não ajudam ninguém. Façam pausas, peçam ajuda, aceitem que não vão acertar sempre.

No final, o que importa é o amor, é estar presente, é mostrar que se importa. A tecnologia é só mais um desafio na linda e difícil arte de educar um filho. Com amor, paciência e diálogo, a gente supera.
EOF

# PROJETO 3 - Terceira transcrição
cat > projects/$PROJ3/arquivos/diretor_escola_publica.txt << 'EOF'
Entrevistador: Como diretor de escola pública, quais os principais desafios na implementação de tecnologia educacional?

Diretor: Rapaz, por onde eu começo? Os desafios são enormes, mas vou tentar organizar as ideias. Primeiro e mais óbvio: recursos. Escola pública vive de migalhas, e tecnologia é cara. Não é só comprar computador, é manutenção, é internet de qualidade, é capacitação, é suporte técnico. O orçamento mal dá pra papel higiênico, imagine pra tecnologia de ponta.

Mas sabe o que mais me frustra? Quando conseguimos algum recurso, muitas vezes vem de cima pra baixo, sem considerar nossa realidade. Já recebi tablet que não funcionava porque nossa internet não aguentava. Já veio software maravilhoso que não rodava nos computadores jurássicos que temos. É um desperdício.

Entrevistador: E como vocês lidam com essas limitações?

Diretor: Criatividade e parceria, meu amigo. Muita criatividade e parceria. Fizemos acordos com universidades pra estágio de alunos de TI que nos ajudam com manutenção. Conseguimos doação de equipamentos usados de empresas. Professor aprendeu a ser técnico de informática nas horas vagas.

Uma coisa que funcionou foi o BYOD - Bring Your Own Device. Os alunos usam seus próprios celulares. Não é ideal, mas é o que temos. Claro que isso escancara a desigualdade. Tem aluno com iPhone último modelo e aluno sem nenhum dispositivo. Aí criamos um sistema de compartilhamento, rodízio de uso do laboratório, empréstimo de equipamentos.

E investimos muito em formação. De que adianta ter tecnologia se o professor não sabe usar? Mas formação também custa, e tempo de professor é escasso. Então fazemos formação em horário de planejamento, aos sábados, online. É puxado, mas necessário.

Entrevistador: Qual o impacto pedagógico que você observa?

Diretor: Quando funciona, é transformador. Já vi aluno que não se interessava por nada descobrir programação e hoje está na universidade. Vi professora de 60 anos aprender a usar lousa digital e renovar completamente suas aulas. São histórias que me emocionam.

Mas também vejo o lado negativo. A exclusão digital é real e cruel. O aluno que não tem acesso fica ainda mais para trás. A pandemia escancarou isso. Tive aluno que sumiu por meses porque não tinha como acompanhar aula online. Quando voltou, estava completamente perdido.

E tem a questão da qualidade pedagógica. Tecnologia mal usada é pior que não ter tecnologia. Já vi professor que só mudou o quadro negro pelo PowerPoint, continua a mesma aula expositiva chata. Ou pior, professor que passa vídeo do YouTube a aula toda porque não quer preparar aula.

Entrevistador: Como você vê o futuro da educação pública com tecnologia?

Diretor: Sou realista otimista, se é que isso existe. Sei que os desafios são gigantes, que a desigualdade no Brasil é gritante, que falta investimento, que falta política pública séria. Mas também vejo potencial imenso.

A tecnologia pode ser a grande equalizadora se bem utilizada. Pode levar educação de qualidade pro interior do Amazonas, pode personalizar ensino pro aluno com dificuldade, pode abrir portas que antes eram fechadas. Mas pra isso precisa de investimento sério, de política de Estado, não de governo.

Precisa também mudar a mentalidade. Parar de ver tecnologia como salvadora ou como vilã. É ferramenta, e ferramenta é tão boa quanto quem a usa. Precisamos formar professores, não só em tecnologia, mas em pedagogia digital. Precisamos infraestrutura decente, não só computador, mas internet, energia elétrica estável, segurança.

E precisamos ouvir a comunidade escolar. Aluno, professor, família, todo mundo tem que participar. Solução de gabinete não funciona. Cada escola tem sua realidade, suas necessidades, suas possibilidades.

Entrevistador: Que mensagem você deixaria?

Diretor: Que não desistam. Sei que é difícil, sei que parece impossível às vezes. Mas educação é a única saída pra esse país, e tecnologia bem aplicada pode acelerar essa transformação. Cada pequeno avanço importa. Cada aluno que aprende algo novo importa. Cada professor que se supera importa.

E cobrem. Cobrem dos governantes, cobrem investimento, cobrem política séria. Educação não pode ser moeda de troca política, tem que ser prioridade de verdade. Tecnologia na educação não é luxo, é necessidade no século XXI.

Mas enquanto as coisas não mudam lá em cima, a gente vai fazendo o que pode aqui embaixo. Com garra, com criatividade, com amor pela educação. Porque no final, é disso que se trata. Amor pela educação, pela transformação de vidas. A tecnologia é só mais uma ferramenta nessa missão.
EOF

echo "🔍 Analisando projetos..."
python run_analysis.py --project $PROJ1
python run_analysis.py --project $PROJ2
python run_analysis.py --project $PROJ3

echo "📊 Comparando..."
python run_analysis.py --compare $PROJ1 $PROJ2 $PROJ3


if [ "$OPEN_RESULTS" = "yes" ]; then
    # Pegar o arquivo PNG mais recente
    LATEST_PNG=$(ls -t projects/comparisons/*_test.png 2>/dev/null | head -1)
    if [ -f "$LATEST_PNG" ]; then
        echo "📊 Abrindo gráfico comparativo: $(basename $LATEST_PNG)"
        open "$LATEST_PNG"
    else
        echo "⚠️ Nenhum arquivo PNG de teste encontrado"
    fi
fi

echo "🎉 Teste completo com transcrições densas finalizado!"
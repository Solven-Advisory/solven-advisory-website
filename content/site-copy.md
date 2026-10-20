# Site copy: English and Portuguese

Every piece of text on the site v5 pages, except the insight articles (content/insights/), lives here.
Each entry has a name (### ...), sometimes a note on where it appears (> ...), then the English
(EN:) and the Portuguese (PT:). Edit either line, then rebuild:

    python3 tools/build_site_v5.py

Rules:
- A text may run over several lines; the lines are joined with a space. A blank line ends it.
- Write the email address as it is; the page turns it into a link. Other links: [text](https://...).
- **bold** and *italic* work. Never use an em dash.
- [[text]] is a placeholder for a fact still to come: the page shows it marked as dummy text, and the
  production build lists every placeholder left. Replace the whole [[...]] with the real text.
- Keep the ### names as they are: the build reads them. If an entry is missing, misnamed, or has
  no EN or PT line, the build stops and says which one.
- Headings (# and ##) and notes (>) are only for finding your way; the build ignores them.

# Every page

Header, footer and the closing band that ends Home and Insights.

## Navigation (header, footer, buttons)

### nav.home
> Footer link
EN: Home
PT: Início

### nav.insights
> Header and footer link, and the 404 page link
EN: Insights
PT: Insights

### nav.book
> Every Book a call button and link
EN: Book a call
PT: Marcar uma chamada

## Footer

### footer.legal
> After "© 2026 Solven Advisory, Lda" at the foot of every page
EN: NIPC [[NIPC]] · [[Registered office address]]
PT: NIPC [[NIPC]] · Sede: [[Morada da sede]]

### footer.city
EN: Lisbon, Portugal
PT: Lisboa, Portugal

### footer.privacy
EN: Privacy
PT: Privacidade

## Closing band (Home and Insights)

### close.title
EN: The edge is where the advantage is.
PT: É na fronteira que está a diferença.

### close.text
EN: What comes next in AI is still unwritten. We work at that edge every month, so your firm and its portfolio can step onto new ground without losing their footing.
PT: O futuro da IA ainda está por escrever. Trabalhamos nessa vanguarda todos os meses, para que a sua empresa e as suas participadas possam explorar novos horizontes sem perder o equilíbrio.

### close.write
> Link beside the button; opens an email
EN: Write to us
PT: Enviar-nos um email

## Hidden labels (read by screen readers and shown as tooltips, not on the page)

### label.skip
> First link on every page, visible only when tabbing with the keyboard
EN: Skip to content
PT: Saltar para o conteúdo

### label.logo
> The logo link
EN: Solven Advisory, home
PT: Solven Advisory, início

### label.menu
> Phone menu button
EN: Menu
PT: Menu

### label.menu_close
> Phone menu button when open
EN: Close
PT: Fechar

### label.nav
> Name of the header navigation
EN: Main
PT: Principal

### label.footer_nav
> Name of the footer navigation
EN: Footer
PT: Rodapé

### label.language
> Name of the EN/PT switch
EN: Language
PT: Idioma

### label.linkedin
> LinkedIn icon
EN: Solven Advisory on LinkedIn
PT: Solven Advisory no LinkedIn

### label.email
> Envelope icon
EN: Email Solven Advisory
PT: Enviar um email à Solven Advisory

### label.dummy_text
> Tooltip on yellow placeholder text
EN: Dummy text: replace before launch
PT: Texto provisório: substituir antes do lançamento

### label.dummy_date
> Tooltip on yellow placeholder dates
EN: Dummy date: replace before launch
PT: Data provisória: substituir antes do lançamento


# Home

## Browser tab, search results and link previews

### home.tab_title
EN: Solven Advisory · AI enablement and implementation for investment firms
PT: Solven Advisory · Formação e implementação de IA em empresas de investimento

### home.description
EN: Solven Advisory trains private equity teams on AI, builds it into their workflows, and runs AI projects in portfolio companies that lift EBITDA.
PT: A Solven Advisory forma equipas de capital de investimento em IA, integra-a nos seus fluxos de trabalho e implementa projetos de IA que aumentam o EBITDA.

### home.ld_description
> Description for search engines (structured data), not shown on the page
EN: Solven Advisory trains private equity teams on AI, builds AI systems on their workflows, runs AI projects in their portfolio companies that lift EBITDA.
PT: A Solven Advisory forma equipas de capital de investimento em IA, integra-a nos seus fluxos de trabalho e implementa projetos de IA nas empresas do seu portfólio que aumentam o EBITDA.

### home.ld_topics
> Topics for search engines (structured data), separated by commas
EN: AI enablement, Private equity workflows, Portfolio value creation, Token economics, Anthropic Claude, OpenAI ChatGPT
PT: Formação em IA, Workflows em private equity, Criação de valor no portfólio, Economia de tokens, Anthropic Claude, OpenAI ChatGPT

## Hero

### home.hero.title
EN: Sharper judgment for the age of AI.
PT: Um critério mais apurado, na era da IA.

### home.hero.text
EN: Solven trains private equity teams on AI, builds it into their workflows, and runs projects across their portfolio companies that lift EBITDA. The people making the call still own the reasoning behind it.
PT: A Solven forma equipas de private equity em IA, integra-a nos seus processos e implementa projetos que aumentam o EBITDA das participadas. As decisões, e o raciocínio por trás delas, continuam nas mãos de quem decide.

## Services

### home.services.title
EN: Four ways we work with a firm.
PT: Como podemos trabalhar juntos.

### home.service1.name
EN: Enablement
PT: Formação

### home.service1.text
EN: Hands-on sessions on the leading AI platforms for the whole firm, analyst to managing partner, run monthly because the frontier moves weekly.
PT: Sessões práticas nas principais plataformas de IA para toda a empresa, desde os analistas até aos sócios-gerentes, todos os meses, porque a inovação acontece todas as semanas.

### home.service2.name
EN: Build
PT: Implementação

### home.service2.text
EN: Agents and workflow systems on the fund's own work: contract redlining, IC memo interrogation, portfolio reporting.
PT: Agentes e workflows aplicados ao fundo: revisão de contratos, análise de memorandos de consultores independentes e elaboração de relatórios sobre o portfólio

### home.service3.name
EN: Portfolio
PT: Portfólio

### home.service3.text
EN: For any portfolio company, in any sector: we find what is holding back EBITDA and fix it, with AI where it helps and without it where it does not.
PT: Para qualquer empresa do nosso portfólio, em qualquer setor: identificamos o que está a limitar o EBITDA e resolvemos o problema, recorrendo à IA quando é útil e prescindindo dela quando não é.

### home.service4.name
EN: Token Economics
PT: Economia de tokens

### home.service4.text
EN: Where the compute spend goes, what it returns, and how to pace it so the year's budget lasts the year.
PT: Para onde vai a despesa da IA, o que rende e como a dosear para que o orçamento do ano dure o ano inteiro.

## Convictions (dark band)

### home.thesis
EN: Augmentation without cognitive atrophy.
PT: Ampliar capacidades, preservando o pensamento crítico.

### home.conviction1.title
EN: Judgment is the product.
PT: O critério é o produto.

### home.conviction1.text
EN: In an investment firm the deliverable is a defensible decision; AI should make that judgment sharper, never thinner.
PT: Numa empresa de investimento, o resultado esperado é uma decisão fundamentada; a IA deve tornar esse julgamento mais preciso, nunca mais superficial.

### home.conviction2.title
EN: Fluency is firm-wide.
PT: A fluência fica presente em toda a empresa

### home.conviction2.text
EN: From the newest analyst to the managing partner, everyone should know where AI belongs in their own work, and where it does not.
PT: Do analista mais recente ao sócio-gerente, todos devem saber onde a IA tem lugar no seu próprio trabalho, e onde não tem.

### home.conviction3.title
EN: The portfolio is where it pays.
PT: É no portfólio que compensa.

### home.conviction3.text
EN: Whatever its sector, every portfolio company has a part of the business holding it back. We start from that problem, not from the technology.
PT: Seja qual for o setor, cada empresa do portfólio tem uma parte do negócio que a está a travar. Partimos desse problema, não da tecnologia.

## Insights

### home.insights.title
> Also the title of the Insights page
EN: Insights.
PT: Insights.

### home.insights.text
EN: Short notes on AI in investment firms: what we see in the work, and what it means for partners.
PT: Notas curtas sobre IA em empresas de investimento: o que vemos no trabalho, e o que isso significa para os partners.

### insights.all
> Button on the homepage, link under every article
EN: All insights
PT: Todos os insights


# Insights page and articles

The articles themselves are in content/insights/ and content/insights/pt/.

### insights.tab_title
EN: Insights · Notes on AI for investment firms · Solven Advisory
PT: Insights · Notas sobre IA para empresas de investimento · Solven Advisory

### insights.description
EN: Short notes from Solven Advisory on AI in private equity, real estate and venture firms: what we see in the work, and what it means for partners.
PT: Notas curtas da Solven Advisory sobre IA em private equity, imobiliário e venture capital: o que vemos no nosso trabalho e o que pode trazer aos sócios.

### insights.ld_name
> Name for search engines (structured data)
EN: Solven Advisory insights
PT: Insights da Solven Advisory

### article.tab_title
> {title} is replaced by the article's title
EN: {title} · Insights · Solven Advisory
PT: {title} · Insights · Solven Advisory

### article.byline
> First of the article tags
EN: By Solven Advisory
PT: Por Solven Advisory

### article.updated
> Article tags, only when the insight has an updated: date; {date} is replaced by it
EN: Updated {date}
PT: Atualizado a {date}

### article.service
> Under the article's buttons; {service} is replaced by the service's name, linked to it on the homepage
EN: Our work on this: {service}.
PT: O nosso trabalho nesta área: {service}.

### article.related
> Heading of the two related insights at the end of each article
EN: More insights.
PT: Mais insights.

### article.minutes
> Article tags and cards; {n} is replaced by the number of minutes
EN: {n} min read
PT: {n} min de leitura

### article.label
> Hidden label of the article section
EN: Article
PT: Artigo

### article.tags_label
> Hidden label of the tags
EN: About this insight
PT: Sobre esta publicação

### article.image_missing
> Placeholder until a photograph is chosen
EN: Image to be chosen
PT: Imagem por escolher

### article.image_missing_note
> Tooltip on that placeholder
EN: Placeholder: choose a photograph for this insight
PT: Provisório: escolher uma fotografia para esta publicação


# Book a call

### book.tab_title
EN: Book a call · Solven Advisory
PT: Marcar uma chamada · Solven Advisory

### book.description
EN: Book thirty minutes with a Solven Advisory co-founder, by video or phone.
PT: Marque uma reunião de trinta minutos com um dos cofundadores da Solven Advisory, por vídeo ou por telefone.

### book.title
EN: Book a call.
PT: Marcar uma chamada.

### book.text
> Beside the title: what the call covers
EN: Thirty minutes with a co-founder, by video or phone: your firm, the work you want AI to help with, and whether one of our four services fits.
PT: Trinta minutos com um dos cofundadores, por vídeo ou por telefone: a vossa casa de investimento, o trabalho em que querem a ajuda da IA e se algum dos nossos quatro serviços se adequa.

### book.calendar_label
> Hidden label of the calendar
EN: Calendar
PT: Calendário

### book.fallback
> Under the calendar; the link opens Cal.com in a new tab
EN: If the calendar does not load, [open it in a new tab](https://cal.eu/miguelmonteirosolven/30min).
PT: Se o calendário não carregar, [abram-no num novo separador](https://cal.eu/miguelmonteirosolven/30min).

### book.write
> Followed by the envelope icon
EN: Prefer to write?
PT: Prefere escrever?

## Questions (under the calendar; the FAQPage structured data uses the same text)

### book.faq.title
EN: Common questions.
PT: Perguntas frequentes.

### book.faq1.q
EN: Who do you work with?
PT: Com quem trabalham?

### book.faq1.a
EN: Private equity firms first, and also real estate and venture firms, across Iberia and the rest of Europe. Portfolio work is for their portfolio companies, in any sector.
PT: Com sociedades de private equity em primeiro lugar, e também de imobiliário e de venture capital, na Península Ibérica e no resto da Europa. O trabalho de portfólio é para as empresas participadas, em qualquer setor.

### book.faq2.q
EN: How is an engagement priced?
PT: Como é definido o preço?

### book.faq2.a
EN: Each engagement is scoped and priced individually: a six-person deal team and a forty-person firm are not the same engagement. Enablement runs monthly with no minimum commitment, so the decision you are making is a month's decision, not a year's.
PT: Cada colaboração é dimensionada e orçamentada individualmente: uma equipa de seis pessoas e uma casa com quarenta não são a mesma colaboração. A formação é mensal e sem compromisso mínimo, pelo que a decisão que estão a tomar é a de um mês, não a de um ano.

### book.faq3.q
EN: How much of the team's time does it take?
PT: Quanto tempo da equipa exige?

### book.faq3.a
EN: Enablement starts with four sessions in the first month, from how a model thinks through to building with it; from month two the cadence is monthly, on the areas the team finds most valuable. Sessions run on your own deals, models and memos, so the time goes into the actual work rather than beside it. Build and Portfolio work is scoped project by project, and the timeline is agreed before it starts.
PT: A formação começa com quatro sessões no primeiro mês, de como um modelo pensa até à construção com ele; a partir do segundo mês, a cadência é mensal, aprofundando as áreas que a equipa considera mais valiosas. As sessões correm sobre os vossos próprios negócios, modelos e memorandos, pelo que o tempo é investido no trabalho real e não ao lado dele. O trabalho de implementação e de portfólio é dimensionado projeto a projeto, com o calendário acordado antes de começar.

### book.faq4.q
EN: What happens to our firm's data?
PT: O que acontece aos dados da nossa casa?

### book.faq4.a
EN: The work runs on your actual deals, models and memos, so this question deserves a precise answer rather than a reassuring one. Data handling is settled during scoping, before any material is opened: whose accounts the work passes through, on what terms, and what, if anything, is retained afterwards. The answers are put in writing before work starts.
PT: O trabalho corre sobre os vossos negócios, modelos e memorandos reais, pelo que esta pergunta merece uma resposta precisa e não apenas tranquilizadora. O tratamento de dados é definido durante o scoping, antes de qualquer material ser aberto: por que contas passa o trabalho, em que termos, e o que é retido depois, se alguma coisa for. As respostas ficam por escrito antes de o trabalho começar.

### book.faq5.q
EN: Are we locking ourselves into one AI vendor?
PT: Ficamos presos a um único fornecedor de IA?

### book.faq5.a
EN: No. The first session teaches how any large model works, from tokens, attention and probability to where hallucinations come from, and the verification habits we build are model-agnostic. If the market shifts, the fluency travels with your team.
PT: Não. A primeira sessão ensina como funciona qualquer modelo de grande dimensão, dos tokens, atenção e probabilidade à origem das alucinações, e os hábitos de verificação que construímos são independentes do modelo. Se o mercado mudar, a fluência viaja com a vossa equipa.

### book.faq6.q
EN: Is the work done in Portuguese or English?
PT: O trabalho é feito em português ou em inglês?

### book.faq6.a
EN: Either, or both. We are based in Lisbon and work with firms from Lisbon to London, so sessions run in the language the room prefers. Written materials are in English, because the tools and the frontier are.
PT: Uma das duas, ou ambas. Estamos sediados em Lisboa e trabalhamos com casas de Lisboa a Londres, pelo que as sessões decorrem na língua que a sala preferir. Os materiais escritos são em inglês, porque as ferramentas e a fronteira o são.

### book.faq7.q
EN: Will this make our analysts dependent on AI?
PT: Isto vai tornar os nossos analistas dependentes da IA?

### book.faq7.a
EN: That risk is the reason Solven exists. The failure mode in most rollouts is not adoption failure; it is analysts becoming editors of drafts they cannot defend. Every session is built the other way round: the analyst produces a defensible first pass, then brings the model in as a critic, a red-teamer and a verifier. Used this way, it sharpens exactly the skills that unconstrained use erodes.
PT: Esse risco é a razão de a Solven existir. O modo de falha da maioria dos rollouts não é a adoção falhar; é os analistas tornarem-se editores de rascunhos que não conseguem defender. Cada sessão é construída ao contrário: o analista produz primeiro uma análise defensável, e só depois traz o modelo como crítico, red-teamer e verificador. Usado assim, o modelo afia exatamente as competências que o uso sem critério corrói.

### book.faq8.q
EN: Why Solven rather than a large consultancy, or doing it in-house?
PT: Porquê a Solven e não uma grande consultora, ou fazer isto internamente?

### book.faq8.a
EN: The work is specific: we work only with investment firms, on your deals and memos rather than a generic curriculum. The cadence is the product: the technology shifts weekly, so a one-off training project is stale within a quarter. And we design against cognitive offloading, so judgment gets sharper rather than thinner. If what a firm mainly needs is change management across a thousand seats, a large consultancy is the right call, and we will say so.
PT: O trabalho é específico: trabalhamos apenas com casas de investimento, sobre os vossos negócios e memorandos, não sobre um currículo genérico. A cadência é o produto: a tecnologia muda semanalmente, e um projeto de formação pontual fica desatualizado num trimestre. E desenhamos contra o offloading cognitivo, para que o critério fique mais afiado e não mais fino. Se o que uma casa precisa sobretudo é de gestão da mudança em mil postos, uma grande consultora é a escolha certa, e di-lo-emos.


# Privacy

### privacy.tab_title
EN: Privacy · Solven Advisory
PT: Privacidade · Solven Advisory

### privacy.description
EN: How Solven Advisory handles the personal data of the people who write to us or book a call. This site sets no cookies of its own.
PT: Como a Solven Advisory trata os dados pessoais de quem nos escreve ou marca uma chamada. Este site não instala cookies próprios.

### privacy.title
EN: Plain terms for personal data.
PT: Termos claros sobre dados pessoais.

### privacy.text
EN: No marketing list, no advertising, and no tracking cookies. This page says what we do hold, why, and for how long.
PT: Sem lista de marketing, sem publicidade e sem cookies de rastreamento. Esta página diz o que guardamos, porquê e durante quanto tempo.

### privacy.scope
EN: This notice covers the personal data of people who visit this site, write to us, or book a call.
PT: Este aviso abrange os dados pessoais de quem visita este site, nos escreve ou marca uma chamada.

### privacy.updated
> Followed by the date below
EN: Last updated
PT: Última atualização:

### privacy.updated_date
> Write the English date as day, month in full, year: the page reads it as the date
EN: 20 October 2026
PT: 20 de outubro de 2026

### privacy.label
> Hidden label of the notice
EN: Privacy notice
PT: Aviso de privacidade

## Section 1

### privacy.s1.title
EN: Who we are
PT: Quem somos

### privacy.s1.p1
EN: Solven Advisory is an AI enablement and implementation consultancy based in Lisbon, Portugal. For anything in this notice, the controller you are dealing with is Solven Advisory, Lda, NIPC [[NIPC]], with its registered office at [[registered office address]], and the fastest route is miguelmonteiro@solvenadvisory.ai.
PT: A Solven Advisory é uma consultora de formação e implementação de IA sediada em Lisboa, Portugal. Para tudo o que consta deste aviso, o responsável pelo tratamento é a Solven Advisory, Lda, NIPC [[NIPC]], com sede em [[morada da sede]], e a forma mais rápida de nos contactar é miguelmonteiro@solvenadvisory.ai.

## Section 2

### privacy.s2.title
EN: What we collect, and why
PT: O que recolhemos, e porquê

### privacy.s2.p1
EN: If you book a call, scheduling runs on Cal.com's EU-hosted infrastructure, which collects the name, email address, and time slot you provide in order to place the meeting in both calendars. If you simply email or phone us, we hold the correspondence the way any firm holds its mail.
PT: Se marcar uma chamada, o agendamento corre na infraestrutura da Cal.com alojada na UE, que recolhe o nome, o endereço de email e o horário que indicar, para colocar a reunião em ambos os calendários. Se apenas nos enviar um email ou telefonar, guardamos a correspondência como qualquer empresa guarda o seu correio.

### privacy.s2.p2
EN: We run Vercel's cookieless analytics, which counts visits in aggregate, stores nothing on your device, and does not identify individuals.
PT: Usamos a análise de audiências sem cookies da Vercel, que conta as visitas de forma agregada, não guarda nada no seu dispositivo e não identifica ninguém.

### privacy.s2.p3
EN: This site sets no cookies of its own, so there is nothing to accept. The booking calendar is served by Cal.com, which sets one strictly necessary security cookie (Cloudflare's __cf_bm, kept for about 30 minutes) to filter automated traffic; it is not used to follow you. The typefaces are served from this site, so no request goes to Google. There is no advertising, no profiling, and no data sold or passed to brokers. There is no newsletter and no marketing list; when we say we reply to people, not leads, this notice is what that means in practice.
PT: Este site não instala cookies próprios, por isso não há nada a aceitar. O calendário de marcações é servido pela Cal.com, que instala um único cookie de segurança estritamente necessário (o __cf_bm, da Cloudflare, guardado durante cerca de 30 minutos) para filtrar tráfego automatizado; não é usado para seguir a sua navegação. Os tipos de letra são servidos por este site, pelo que nenhum pedido segue para a Google. Não há publicidade, nem definição de perfis, nem dados vendidos ou cedidos a corretores de dados. Não há newsletter nem lista de marketing; quando dizemos que respondemos a pessoas, e não a leads, este aviso é o que isso significa na prática.

## Section 3

### privacy.s3.title
EN: The legal basis
PT: O fundamento jurídico

### privacy.s3.p1
EN: We process booking details and correspondence because you asked us to: steps taken at your request before a possible contract (Article 6(1)(b) of the GDPR). We keep ordinary business correspondence on the basis of legitimate interest (Article 6(1)(f)). Aggregate visit counts rest on the same legitimate interest, in knowing how the site is read. The calendar's security cookie is strictly necessary for a service you asked for, which Lei 41/2004 exempts from consent.
PT: Tratamos os dados de marcação e a correspondência porque nos pediu que o fizéssemos: diligências pré-contratuais a seu pedido (artigo 6.º, n.º 1, alínea b), do RGPD). Conservamos a correspondência comercial corrente com base no interesse legítimo (artigo 6.º, n.º 1, alínea f)). As contagens agregadas de visitas assentam no mesmo interesse legítimo, o de saber como o site é lido. O cookie de segurança do calendário é estritamente necessário para um serviço que pediu, o que a Lei n.º 41/2004 isenta de consentimento.

## Section 4

### privacy.s4.title
EN: Where the data sits
PT: Onde ficam os dados

### privacy.s4.p1
EN: The site is hosted by Vercel. Scheduling runs on Cal.com (EU infrastructure). Our email runs on Microsoft 365. Each of these providers acts as a processor for the data described above; none of them is given your details for any purpose beyond delivering the service.
PT: O site está alojado na Vercel. O agendamento corre na Cal.com (infraestrutura na UE). O nosso email corre no Microsoft 365. Cada um destes prestadores atua como subcontratante para os dados acima descritos; a nenhum deles são cedidos os seus dados para qualquer finalidade além da prestação do serviço.

## Section 5

### privacy.s5.title
EN: How long we keep it
PT: Durante quanto tempo os guardamos

### privacy.s5.p1
EN: Correspondence is kept for as long as a working relationship, or the reasonable prospect of one, exists, and afterwards only as long as ordinary business record-keeping requires. If you would like something deleted sooner, ask.
PT: A correspondência é conservada enquanto existir uma relação de trabalho, ou uma perspetiva razoável de a vir a ter, e depois apenas durante o tempo que a conservação normal de registos comerciais exigir. Se preferir que algo seja apagado mais cedo, basta pedir.

## Section 6

### privacy.s6.title
EN: Your rights
PT: Os seus direitos

### privacy.s6.p1
EN: You can ask for access to the data we hold about you, have it corrected or deleted, restrict or object to its processing, and receive a copy in a portable format. Write to miguelmonteiro@solvenadvisory.ai and we will deal with it directly. You also have the right to complain to the Portuguese supervisory authority, the CNPD, at [cnpd.pt](https://www.cnpd.pt).
PT: Pode pedir o acesso aos dados que temos sobre si, a sua retificação ou apagamento, a limitação do tratamento ou opor-se a ele, e receber uma cópia num formato portável. Escreva para miguelmonteiro@solvenadvisory.ai e tratamos do assunto diretamente. Tem também o direito de apresentar reclamação à autoridade de controlo portuguesa, a CNPD (Comissão Nacional de Proteção de Dados), em [cnpd.pt](https://www.cnpd.pt).


# Page not found (404)

### notfound.tab_title
EN: Page not found · Solven Advisory
PT: Página não encontrada · Solven Advisory

### notfound.description
EN: There is nothing at this address.
PT: Não há nada neste endereço.

### notfound.title
EN: There is nothing at this address.
PT: Não há nada neste endereço.

### notfound.text
EN: The page may have moved when the site did, or the address may have a typo in it. Either way, the work continues at the pages below.
PT: A página pode ter mudado de sítio quando o site mudou, ou o endereço pode ter uma gralha. Seja como for, o trabalho continua nas páginas abaixo.

### notfound.back
EN: Back to the start
PT: Voltar ao início

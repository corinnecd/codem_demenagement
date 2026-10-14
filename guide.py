"""Le guide CODEM : rubrique « Conseils et astuces » (articles indexables, un par sujet).
Les informations administratives sont vérifiées sur les sources officielles citées en bas de chaque article."""
import json
import build as b
from build import t,url,link,img,eyebrow,label

MAJ=('14 octobre 2026','14 October 2026')

THEMES={
 'preparer':('Bien préparer','Getting ready'),
 'demarches':('Démarches','Paperwork'),
 'emballage':('Emballage & astuces','Packing tips'),
 'budget':('Budget','Budget'),
 'etranger':('Partir à l’étranger','Moving abroad'),
 'entreprises':('Entreprises','Businesses'),
}

SP='https://www.service-public.gouv.fr/particuliers/vosdroits/'

ARTICLES=[
dict(key='checklist',slug=('checklist-demenagement','moving-checklist'),theme='preparer',photo='particulier-emballage',mn=6,svc='particuliers',
 title=('La checklist complète de votre déménagement','The complete moving checklist'),
 lead=('De deux mois avant le départ au premier mois dans votre nouveau logement : tout ce qu’il faut faire, dans le bon ordre, sans rien oublier.','From two months before you leave to your first month in the new home: everything to do, in the right order, without missing a thing.'),
 sections=[
  (('De J-60 à J-30 : poser les bases','60 to 30 days before: the groundwork'),
   ('<ul><li><strong>Demandez vos devis</strong> et une visite technique, à domicile ou en vidéo. Un devis établi après visite est plus juste qu’une estimation au téléphone.</li><li><strong>Donnez congé à votre bailleur</strong> si vous êtes locataire : 3 mois pour un logement vide, 1 mois pour un meublé ou dans certains cas (zone tendue, mutation, premier emploi…). Voir notre <a href="{g:adresse}">guide des démarches</a>.</li><li><strong>Faites le tri</strong> : vendre, donner, recycler. Chaque objet en moins, c’est du volume et du temps en moins.</li><li><strong>Prévoyez un garde-meubles</strong> si les dates de sortie et d’entrée ne coïncident pas.</li></ul>',
    '<ul><li><strong>Request your quotes</strong> and a survey, at home or by video. A quote made after a survey is more accurate than a phone estimate.</li><li><strong>Give notice to your landlord</strong> if you rent: 3 months for an unfurnished home, 1 month for a furnished one or in certain cases (high-demand area, job transfer, first job…). See our <a href="{g:adresse}">paperwork guide</a>.</li><li><strong>Declutter</strong>: sell, donate, recycle. Every item less means less volume and less time.</li><li><strong>Plan storage</strong> if your move-out and move-in dates do not match.</li></ul>')),
  (('De J-30 à J-15 : organiser','30 to 15 days before: getting organised'),
   ('<ul><li><strong>Confirmez la date et la formule</strong> : qui emballe, qui démonte, qui remonte.</li><li><strong>Demandez l’autorisation de stationnement</strong> pour le camion, aux deux adresses. À Paris, la demande se fait au moins 15 jours avant. Voir <a href="{g:stationnement}">notre guide du stationnement</a>.</li><li><strong>Commencez les cartons</strong> par ce qui ne sert pas : livres, décoration, vêtements de saison.</li><li><strong>Prévenez l’école</strong> et, si besoin, votre employeur : certaines conventions collectives prévoient un congé pour déménagement.</li></ul>',
    '<ul><li><strong>Confirm the date and package</strong>: who packs, who dismantles, who reassembles.</li><li><strong>Request a parking permit</strong> for the truck at both addresses. In Paris, apply at least 15 days ahead. See <a href="{g:stationnement}">our parking guide</a>.</li><li><strong>Start packing</strong> what you do not use: books, decorations, out-of-season clothes.</li><li><strong>Tell the school</strong> and, if needed, your employer: some collective agreements provide moving leave.</li></ul>')),
  (('De J-15 à la veille : boucler','15 days to the day before: wrapping up'),
   ('<ul><li><strong>Déclarez votre changement d’adresse</strong> en ligne : un seul formulaire pour plusieurs organismes.</li><li><strong>Transférez ou résiliez</strong> électricité, gaz, eau, internet et assurance habitation, avec une date précise.</li><li><strong>Videz et dégivrez</strong> réfrigérateur et congélateur la veille.</li><li><strong>Gardez avec vous</strong> papiers importants, bijoux, ordinateurs et médicaments : ils ne voyagent pas dans le camion.</li></ul>',
    '<ul><li><strong>Report your change of address</strong> online: one form for several organisations.</li><li><strong>Transfer or cancel</strong> electricity, gas, water, internet and home insurance, with a precise date.</li><li><strong>Empty and defrost</strong> the fridge and freezer the day before.</li><li><strong>Keep with you</strong> important papers, jewellery, computers and medicines: they do not travel in the truck.</li></ul>')),
  (('Le jour J','Moving day'),
   ('<ul><li>Soyez présent, ou une personne de confiance, au départ comme à l’arrivée.</li><li>Relevez les compteurs et faites l’état des lieux de sortie.</li><li>Faites un dernier tour des placards, de la cave et du balcon.</li><li>À l’arrivée, vérifiez les meubles et les cartons avant de signer, et notez immédiatement toute réserve sur le document de livraison.</li></ul>',
    '<ul><li>Be there, or someone you trust, at departure and arrival.</li><li>Read the meters and do the move-out inspection.</li><li>Check cupboards, cellar and balcony one last time.</li><li>On arrival, check furniture and boxes before signing, and write any reservation straight onto the delivery document.</li></ul>')),
  (('Le premier mois','The first month'),
   ('<ul><li><strong>Carte grise</strong> : 1 mois pour y inscrire la nouvelle adresse, en ligne et gratuitement pour les trois premiers changements.</li><li><strong>Liste électorale</strong> : inscription dans votre nouvelle commune.</li><li><strong>Animal identifié</strong> : mettez à jour vos coordonnées dans le fichier I-Cad.</li><li><strong>Médecin traitant</strong> : choisissez-en un plus proche si besoin.</li></ul>',
    '<ul><li><strong>Vehicle registration</strong>: 1 month to add the new address, online and free for the first three changes.</li><li><strong>Electoral roll</strong>: register in your new town.</li><li><strong>Identified pet</strong>: update your details in the I-Cad register.</li><li><strong>GP</strong>: choose one closer to home if needed.</li></ul>')),
 ],
 tip=('Préparez un carton « premiers jours » : chargeurs, papiers, draps, une casserole, du café, le nécessaire de toilette. Fermez-le en dernier, ouvrez-le en premier.','Pack a “first days” box: chargers, papers, sheets, a saucepan, coffee, toiletries. Close it last, open it first.'),
 faq=[(('Combien de temps à l’avance réserver son déménageur ?','How far ahead should I book a mover?'),('Idéalement un à deux mois avant. Les périodes les plus demandées, l’été et les fins de mois, se réservent plus tôt.','Ideally one to two months ahead. The busiest periods, summer and month ends, book up earlier.')),
      (('Faut-il être présent le jour du déménagement ?','Do I need to be there on moving day?'),('Oui, vous ou une personne de confiance, au chargement comme à la livraison, pour indiquer les consignes et vérifier l’arrivée des biens.','Yes, you or someone you trust, at loading and delivery, to give instructions and check your belongings on arrival.'))],
 extra=('<p class="ga-download">Vous préférez une version à cocher ? <a href="{conseils}#checklist-offerte">Recevez la checklist complète en PDF</a>.</p>','<p class="ga-download">Prefer a version to tick off? <a href="{conseils}#checklist-offerte">Get the full checklist as a PDF</a>.</p>'),
 sources=[('Service-Public : je déménage en France',SP+'F14128'),('Service-Public : préavis du locataire',SP+'F1168'),('Service-Public : adresse de la carte grise',SP+'F12118')]),

dict(key='adresse',slug=('changement-adresse-demarches','change-of-address'),theme='demarches',photo='particulier-maison',mn=7,svc='particuliers',
 title=('Changement d’adresse : toutes les démarches','Change of address: every step'),
 lead=('Logement, organismes, énergie, carte grise, vote : qui prévenir, quand et comment, avec les délais officiels.','Housing, public bodies, energy, vehicle, voting: who to tell, when and how, with the official deadlines.'),
 sections=[
  (('Le service en ligne de l’État','The government online service'),
   ('<p>Une démarche en ligne unique permet de signaler votre nouvelle adresse en une fois à plusieurs organismes : l’Assurance maladie (CPAM), les impôts, la Caf, France Travail et EDF. Pensez ensuite à prévenir vous-même votre mutuelle, votre caisse de retraite, votre banque et vos assurances.</p>',
    '<p>A single online service lets you report your new address to several bodies at once: health insurance (CPAM), the tax office, the Caf, France Travail and EDF. Then tell your top-up health insurer, pension fund, bank and insurers yourself.</p>')),
  (('Le logement que vous quittez','The home you are leaving'),
   ('<ul><li><strong>Préavis</strong> : 3 mois pour un logement vide. Il passe à 1 mois en zone tendue, en cas de mutation, de perte d’emploi, de premier emploi ou d’attribution d’un logement social, avec justificatif. Pour un meublé, 1 mois, sans motif.</li><li><strong>Envoi du congé</strong> : lettre recommandée avec accusé de réception, acte de commissaire de justice ou remise en main propre contre signature. Un simple e-mail n’est pas valable.</li><li><strong>Point de départ</strong> : le jour de réception de la lettre par le bailleur.</li><li><strong>Dépôt de garantie</strong> : restitué dans un délai de 1 à 2 mois après la remise des clés, selon l’état des lieux.</li></ul>',
    '<ul><li><strong>Notice</strong>: 3 months for an unfurnished home. It drops to 1 month in high-demand areas, for a job transfer, job loss, first job or social housing allocation, with proof. For a furnished home, 1 month, no reason needed.</li><li><strong>Sending notice</strong>: registered letter with acknowledgement of receipt, bailiff’s deed, or hand delivery against signature. A plain email is not valid.</li><li><strong>Start date</strong>: the day the landlord receives the letter.</li><li><strong>Deposit</strong>: returned within 1 to 2 months of handing back the keys, depending on the inspection.</li></ul>')),
  (('Énergie, eau, internet, courrier','Energy, water, internet, post'),
   ('<ul><li>Transférez ou résiliez vos contrats d’électricité, de gaz et d’eau, en relevant les compteurs le jour du départ.</li><li>Prévenez votre opérateur internet. S’il n’a pas d’offre à votre nouvelle adresse, vous pouvez résilier sans frais pour motif légitime.</li><li>La réexpédition du courrier par La Poste est un service payant, utile les premiers mois.</li></ul>',
    '<ul><li>Transfer or cancel your electricity, gas and water contracts, reading the meters on moving day.</li><li>Tell your internet provider. If it has no offer at your new address, you can cancel free of charge for legitimate reasons.</li><li>Mail forwarding by La Poste is a paid service, useful for the first months.</li></ul>')),
  (('Véhicule et papiers d’identité','Vehicle and ID'),
   ('<ul><li><strong>Carte grise</strong> : vous avez 1 mois pour changer l’adresse, en ligne sur le site de l’ANTS. C’est gratuit pour les trois premiers changements. Passé le délai, l’amende peut atteindre 135 €.</li><li><strong>Permis de conduire</strong> : pas d’obligation de changer l’adresse.</li><li><strong>Carte d’identité et passeport</strong> : ils n’ont pas à être modifiés.</li></ul>',
    '<ul><li><strong>Vehicle registration</strong>: you have 1 month to change the address, online on the ANTS website. It is free for the first three changes. After the deadline, the fine can reach €135.</li><li><strong>Driving licence</strong>: no obligation to change the address.</li><li><strong>ID card and passport</strong>: they do not need to be changed.</li></ul>')),
  (('Vote, enfants, animaux','Voting, children, pets'),
   ('<ul><li><strong>Liste électorale</strong> : inscrivez-vous dans votre nouvelle commune, en ligne ou en mairie (formulaire Cerfa n° 12669).</li><li><strong>École</strong> : demandez le changement d’établissement ou le maintien dans l’ancienne école.</li><li><strong>Chien, chat, furet</strong> : mettez à jour vos coordonnées dans le fichier I-Cad.</li></ul>',
    '<ul><li><strong>Electoral roll</strong>: register in your new town, online or at the town hall (Cerfa form no. 12669).</li><li><strong>School</strong>: request a transfer or to stay at the current school.</li><li><strong>Dog, cat, ferret</strong>: update your details in the I-Cad register.</li></ul>')),
  (('Les aides possibles','Possible support'),
   ('<p>Avec au moins trois enfants, sous conditions, la Caf ou la MSA peut verser une allocation de déménagement, à demander dans les 6 mois. Le Fonds de solidarité pour le logement (FSL) peut aussi aider. Votre convention collective peut prévoir une prise en charge par l’employeur, notamment en cas de mutation.</p>',
    '<p>With at least three children, subject to conditions, the Caf or MSA can pay a moving allowance, to be claimed within 6 months. The Housing Solidarity Fund (FSL) may also help. Your collective agreement may provide employer support, especially for a job transfer.</p>')),
 ],
 tip=('Gardez dès l’arrivée un justificatif de domicile récent, une facture d’énergie par exemple : presque toutes les démarches le demandent.','Keep recent proof of address from day one, an energy bill for instance: almost every procedure asks for it.'),
 faq=[(('Dois-je changer l’adresse sur ma carte d’identité ?','Do I need to change the address on my ID card?'),('Non. La carte d’identité et le passeport n’ont pas à être modifiés après un déménagement.','No. Your ID card and passport do not need to be changed after a move.')),
      (('Quel délai pour la carte grise ?','What is the deadline for the vehicle registration?'),('Un mois après le déménagement, en ligne sur le site de l’ANTS. La démarche est gratuite pour les trois premiers changements d’adresse.','One month after moving, online on the ANTS website. It is free for the first three changes of address.'))],
 sources=[('Service-Public : je déménage en France',SP+'F14128'),('Service-Public : préavis du locataire',SP+'F1168'),('Service-Public : adresse de la carte grise',SP+'F12118')]),

dict(key='mutation',slug=('demenager-mutation-professionnelle','moving-for-a-job-transfer'),theme='demarches',photo='ancien-20',mn=6,svc='particuliers',
 title=('Déménager pour une mutation','Moving for a job transfer'),
 lead=('Changer de région pour son travail : préavis réduit, prise en charge des frais, calendrier serré. Les règles pour les salariés et les agents publics.','Changing region for work: shorter notice, cost coverage, tight schedule. The rules for employees and public servants.'),
 sections=[
  (('Ce que la mutation change pour votre logement','What a transfer changes for your home'),
   ('<p>Si vous louez un logement vide, la mutation professionnelle réduit votre préavis à <strong>1 mois</strong> au lieu de 3, pour un salarié comme pour un fonctionnaire. La mutation doit intervenir à une date proche de l’envoi du congé, et vous joignez un justificatif (attestation de l’employeur, arrêté de mutation). Pour un indépendant ou une profession libérale, le préavis reste de 3 mois.</p>',
    '<p>If you rent an unfurnished home, a job transfer cuts your notice to <strong>1 month</strong> instead of 3, for employees and civil servants alike. The transfer must be close to the date you send notice, and you attach proof (employer letter, transfer order). For the self-employed, notice stays at 3 months.</p>')),
  (('Salariés : ce que l’employeur peut prendre en charge','Employees: what your employer may cover'),
   ('<ul><li>La prise en charge n’est pas automatique : elle dépend de votre contrat, de votre convention collective ou d’un accord d’entreprise. Posez la question à votre service RH avant de choisir votre formule.</li><li>Certaines conventions collectives prévoient aussi un <strong>congé pour déménagement</strong>.</li><li>Les frais de déménagement remboursés par l’employeur dans le cadre d’une mobilité professionnelle peuvent être exonérés de cotisations sociales, dans les limites fixées par l’Urssaf.</li></ul>',
    '<ul><li>Cover is not automatic: it depends on your contract, collective agreement or company agreement. Ask HR before choosing your package.</li><li>Some collective agreements also provide <strong>moving leave</strong>.</li><li>Moving costs reimbursed by the employer for a work relocation can be exempt from social contributions, within limits set by Urssaf.</li></ul>')),
  (('Agents publics : les frais de changement de résidence','Public servants: change of residence costs'),
   ('<ul><li>Les frais peuvent être pris en charge quand vous changez de résidence administrative, dans une autre commune, et que votre résidence familiale change aussi. Paris et les communes limitrophes comptent comme une seule commune.</li><li>La prise en charge comprend les frais de transport des personnes et une <strong>indemnité forfaitaire</strong> pour le mobilier, calculée selon la distance et le volume.</li><li>La demande se fait dans les 12 mois suivant la mutation. L’indemnité peut être versée au plus tôt 3 mois avant le changement de résidence.</li><li>La famille doit vous rejoindre dans les 9 mois suivant votre affectation.</li></ul>',
    '<ul><li>Costs can be covered when your official place of work moves to another town and your family home moves too. Paris and its neighbouring towns count as one town.</li><li>Cover includes travel costs for the household and a <strong>flat-rate allowance</strong> for furniture, based on distance and volume.</li><li>Apply within 12 months of the transfer. The allowance can be paid at the earliest 3 months before the move.</li><li>Your family must join you within 9 months of your posting.</li></ul>')),
  (('Un calendrier serré : comment s’organiser','A tight schedule: how to organise'),
   ('<ul><li><strong>Demandez une visite en vidéo</strong> : elle se cale facilement, même à distance de votre futur poste.</li><li><strong>Gardez un devis écrit et détaillé</strong> : il est souvent demandé pour le dossier de prise en charge.</li><li><strong>Prévoyez un garde-meubles</strong> si vous n’avez pas encore trouvé votre logement dans la nouvelle région.</li><li><strong>Pensez à l’école</strong> des enfants et aux démarches de <a href="{g:adresse}">changement d’adresse</a>.</li></ul>',
    '<ul><li><strong>Ask for a video survey</strong>: easy to schedule, even far from your new job.</li><li><strong>Keep a written, detailed quote</strong>: it is often required for the cost-cover file.</li><li><strong>Plan storage</strong> if you have not yet found a home in the new region.</li><li><strong>Think about school</strong> for the children and your <a href="{g:adresse}">change of address</a> steps.</li></ul>')),
 ],
 tip=('Renseignez-vous sur la prise en charge avant de choisir votre formule : elle peut vous permettre de confier aussi l’emballage à l’équipe.','Check your cost cover before choosing a package: it may let you hand the packing over to the team too.'),
 faq=[(('Mon employeur doit-il payer mon déménagement ?','Does my employer have to pay for my move?'),('Pas automatiquement. Pour un salarié, cela dépend du contrat, de la convention collective ou d’un accord d’entreprise. Pour les agents publics, une prise en charge est prévue sous conditions.','Not automatically. For employees, it depends on the contract, collective agreement or company agreement. For public servants, cover is provided under conditions.')),
      (('Le devis CODEM peut-il servir pour mon dossier ?','Can the CODEM quote be used for my file?'),('Oui. Le devis est écrit et détaillé : volume, prestations et prix. Il peut être joint à votre demande de prise en charge.','Yes. The quote is written and detailed: volume, services and price. You can attach it to your cost-cover request.'))],
 sources=[('Service-Public : préavis du locataire',SP+'F1168'),('Service-Public : frais de changement de résidence des agents publics',SP+'F13896'),('Urssaf : frais professionnels, mobilité','https://www.urssaf.fr/accueil/outils-documentation/taux-baremes/frais-professionnels.html')]),

dict(key='vaisselle',slug=('emballer-vaisselle','packing-crockery'),theme='emballage',photo='ancien-27',mn=4,svc='cartons',
 title=('Bien emballer sa vaisselle','How to pack crockery'),
 lead=('Assiettes, verres, plats : la méthode de nos déménageurs pour que tout arrive entier.','Plates, glasses, dishes: our movers’ method so everything arrives in one piece.'),
 sections=[
  (('Le bon matériel','The right materials'),
   ('<ul><li>Des cartons de petite ou moyenne taille, solides : la vaisselle est lourde.</li><li>Des cartons à séparations pour les verres et les bouteilles.</li><li>Du papier d’emballage blanc et du papier bulle pour les pièces fragiles.</li><li>Du ruban adhésif et un marqueur.</li></ul><p>Toutes ces fournitures sont disponibles chez CODEM : voir <a href="{svc:cartons}">cartons et fournitures</a>.</p>',
    '<ul><li>Small or medium sturdy boxes: crockery is heavy.</li><li>Divided boxes for glasses and bottles.</li><li>White packing paper and bubble wrap for fragile pieces.</li><li>Tape and a marker.</li></ul><p>All these supplies are available from CODEM: see <a href="{svc:cartons}">boxes and supplies</a>.</p>')),
  (('Assiettes et plats','Plates and dishes'),
   ('<ol><li>Garnissez le fond du carton de papier froissé.</li><li>Emballez chaque assiette séparément.</li><li>Rangez-les debout, sur la tranche, comme des disques, et non à plat les unes sur les autres.</li><li>Placez les pièces lourdes en bas, les plus légères au-dessus.</li></ol>',
    '<ol><li>Line the bottom of the box with crumpled paper.</li><li>Wrap each plate separately.</li><li>Stand them on edge, like records, not stacked flat.</li><li>Heavy pieces at the bottom, lighter ones on top.</li></ol>')),
  (('Verres et tasses','Glasses and cups'),
   ('<p>Remplissez l’intérieur de chaque verre de papier, puis enveloppez-le. Glissez-le dans un compartiment, ouverture vers le bas. Pour les tasses, protégez aussi l’anse.</p>',
    '<p>Fill each glass with paper, then wrap it. Slide it into a compartment, opening down. For cups, also protect the handle.</p>')),
  (('Caler, fermer, étiqueter','Fill, close, label'),
   ('<ul><li>Comblez chaque vide avec du papier : rien ne doit bouger.</li><li>Gardez un poids raisonnable : vous devez soulever le carton sans effort.</li><li>Écrivez « FRAGILE », la pièce de destination et le sens du carton sur deux faces.</li></ul>',
    '<ul><li>Fill every gap with paper: nothing should move.</li><li>Keep the weight reasonable: you should lift the box easily.</li><li>Write “FRAGILE”, the destination room and “this way up” on two sides.</li></ul>')),
 ],
 tip=('Une fois le carton fermé, secouez-le doucement : si vous entendez bouger, ajoutez du calage.','Once the box is closed, shake it gently: if you hear movement, add more filling.'),
 faq=[(('Le papier journal convient-il ?','Is newspaper all right?'),('Pour caler, oui. Mais l’encre peut marquer la vaisselle : emballez d’abord dans du papier blanc.','For filling, yes. But the ink can mark crockery: wrap in white paper first.')),
      (('CODEM peut-il emballer pour moi ?','Can CODEM pack for me?'),('Oui. Dès la formule Confort, nos déménageurs fournissent les emballages et emballent vos objets fragiles.','Yes. From the Confort package, our movers supply the packing and wrap your fragile items.'))],
 sources=[]),

dict(key='prix',slug=('prix-demenagement-ile-de-france','moving-cost-paris'),theme='budget',photo='chantier-camion',mn=5,svc='formules',
 title=('Combien coûte un déménagement en Île-de-France ?','How much does a move cost in Greater Paris?'),
 lead=('Nos prix de départ, ce qui fait varier le montant, et comment comparer des devis sans mauvaise surprise.','Our starting prices, what changes the amount, and how to compare quotes without surprises.'),
 sections=[
  (('Nos prix de départ','Our starting prices'),
   ('{prix}','{prix}')),
  (('Ce qui fait varier le prix','What changes the price'),
   ('<ul><li><strong>Le volume</strong>, en mètres cubes : c’est le premier critère.</li><li><strong>La distance</strong> entre les deux adresses.</li><li><strong>Les accès</strong> : étage sans ascenseur, distance de portage, rue étroite, besoin d’un monte-meubles.</li><li><strong>La formule</strong> : plus l’équipe emballe et démonte pour vous, plus elle passe de temps.</li><li><strong>Les objets particuliers</strong> : piano, œuvres d’art, mobilier volumineux.</li><li><strong>Le garde-meubles</strong>, si vos dates ne coïncident pas.</li></ul>',
    '<ul><li><strong>Volume</strong>, in cubic metres: the main factor.</li><li><strong>Distance</strong> between the two addresses.</li><li><strong>Access</strong>: floor without lift, carrying distance, narrow street, need for a furniture lift.</li><li><strong>Package</strong>: the more the team packs and dismantles for you, the more time it spends.</li><li><strong>Special items</strong>: piano, artwork, bulky furniture.</li><li><strong>Storage</strong>, if your dates do not match.</li></ul>')),
  (('Estimer votre volume','Estimating your volume'),
   ('<p>Repère courant : le volume en mètres cubes représente environ la moitié de la surface en mètres carrés, un peu plus si le logement est bien meublé. Pour une estimation fiable, utilisez <a href="{conseils}#volume">notre calculateur pièce par pièce</a>.</p>',
    '<p>A common rule of thumb: the volume in cubic metres is about half the floor area in square metres, a little more if the home is well furnished. For a reliable estimate, use <a href="{conseils}#volume">our room-by-room calculator</a>.</p>')),
  (('Bien comparer des devis','Comparing quotes properly'),
   ('<ul><li>Vérifiez que chaque devis porte sur le même volume et les mêmes prestations.</li><li>Préférez un devis établi après visite : il tient compte des accès réels.</li><li>Demandez comment vos biens sont assurés et ce que couvre la déclaration de valeur.</li><li>Exigez un devis écrit et détaillé.</li></ul>',
    '<ul><li>Check that each quote covers the same volume and the same services.</li><li>Prefer a quote made after a survey: it reflects the real access.</li><li>Ask how your belongings are insured and what the declaration of value covers.</li><li>Insist on a written, detailed quote.</li></ul>')),
  (('Alléger la facture','Keeping the cost down'),
   ('<ul><li>Triez avant le devis : moins de volume, moins de temps.</li><li>Emballez vous-même, avec les formules Self et Self plus.</li><li>Restez souple sur la date si vous le pouvez.</li></ul>',
    '<ul><li>Declutter before the quote: less volume, less time.</li><li>Pack yourself, with the Self and Self plus packages.</li><li>Stay flexible on the date if you can.</li></ul>')),
 ],
 tip=('Un devis sans visite reste une estimation. Chez CODEM, la visite est gratuite et le prix devient ferme ensuite.','A quote without a survey is only an estimate. At CODEM, the survey is free and the price is fixed afterwards.'),
 faq=[(('Le prix peut-il changer le jour J ?','Can the price change on moving day?'),('Le prix est confirmé et ferme après la visite. Signalez avant le jour J tout changement de volume ou d’accès, pour que le devis reste juste.','The price is confirmed and fixed after the survey. Tell us before moving day about any change in volume or access, so the quote stays accurate.')),
      (('Existe-t-il des aides ?','Is there any financial help?'),('Selon votre situation : allocation de déménagement de la Caf pour les familles d’au moins trois enfants, sous conditions, ou prise en charge par l’employeur en cas de mutation.','Depending on your situation: the Caf moving allowance for families with at least three children, subject to conditions, or employer support for a job transfer.'))],
 sources=[('Service-Public : je déménage en France',SP+'F14128')]),

dict(key='stationnement',slug=('stationnement-camion-demenagement','moving-truck-parking'),theme='demarches',photo='rue-paris-monte',mn=4,svc='zones',
 title=('Réserver le stationnement du camion','Reserving parking for the truck'),
 lead=('À Paris et dans le Val-de-Marne, garer un camion de déménagement se prépare. Qui contacter, quand, et quelles informations donner.','In Paris and Val-de-Marne, parking a removal truck needs planning. Who to contact, when, and what to provide.'),
 sections=[
  (('Pourquoi c’est important','Why it matters'),
   ('<p>Un camion garé au pied de l’immeuble, c’est moins de portage, un chargement plus rapide et plus sûr pour vos meubles. Sans autorisation, l’équipe peut devoir se garer loin, et la journée s’allonge.</p>',
    '<p>A truck parked right outside means less carrying and faster, safer loading for your furniture. Without a permit, the team may have to park far away, and the day gets longer.</p>')),
  (('À Paris','In Paris'),
   ('<p>Le stationnement d’un véhicule de déménagement passe par une autorisation d’occupation temporaire (AOT) de la Ville, demandée en ligne au moins 15 jours avant. Elle est nécessaire pour stationner hors de la bande payante, plus de 6 heures, ou pour installer un monte-meubles. Les déménagements sont autorisés de 7 h à 20 h.</p>',
    '<p>Parking a removal vehicle requires a temporary occupation permit (AOT) from the City, requested online at least 15 days ahead. It is needed to park outside paid bays, for more than 6 hours, or to set up a furniture lift. Moves are allowed from 7 am to 8 pm.</p>')),
  (('Dans le Val-de-Marne','In Val-de-Marne'),
   ('<p>Dans les communes du Val-de-Marne, le stationnement d’un camion de déménagement sur la voie publique fait l’objet d’un arrêté municipal, demandé à la mairie avant la date. Sur les routes classées à grande circulation, la demande relève des services de l’État (DRIEAT), en ligne. À Saint-Maur-des-Fossés par exemple, les panneaux sont posés 48 heures avant, et 7 jours avant en zone bleue : mieux vaut anticiper.</p>',
    '<p>In Val-de-Marne towns, parking a removal truck on the street requires a municipal order, requested from the town hall ahead of the date. On roads classed as major traffic routes, the request goes to the State services (DRIEAT), online. In Saint-Maur-des-Fossés for instance, signs go up 48 hours ahead, and 7 days ahead in blue zones: best to plan early.</p>')),
  (('Les informations à préparer','What to have ready'),
   ('<ul><li>L’adresse exacte et l’emplacement souhaité.</li><li>La date et la plage horaire.</li><li>La longueur du véhicule ou le nombre de places : votre conseiller CODEM vous les indique.</li><li>La présence éventuelle d’un monte-meubles.</li></ul>',
    '<ul><li>The exact address and preferred spot.</li><li>The date and time slot.</li><li>The vehicle length or number of spaces: your CODEM adviser gives you these.</li><li>Whether a furniture lift will be used.</li></ul>')),
 ],
 tip=('Faites la demande pour les deux adresses, départ et arrivée. On y pense souvent pour l’une, plus rarement pour l’autre.','Apply for both addresses, departure and arrival. People often think of one and forget the other.'),
 faq=[(('Qui fait la demande, le client ou le déménageur ?','Who applies, the client or the mover?'),('Selon la commune, la demande peut être faite par le client ou par le déménageur. Votre conseiller CODEM vérifie avec vous la bonne démarche et le bon délai.','Depending on the town, the client or the mover can apply. Your CODEM adviser checks the right procedure and timing with you.')),
      (('Et si je n’obtiens pas d’autorisation ?','What if I do not get a permit?'),('Prévenez votre conseiller au plus tôt : le portage, le matériel ou l’horaire peuvent être adaptés.','Tell your adviser as early as possible: carrying, equipment or timing can be adjusted.'))],
 extra=('<p class="ga-download">Règles commune par commune : <a href="{svc:zones}">consultez nos repères sur place</a>.</p>','<p class="ga-download">Town-by-town rules: <a href="{svc:zones}">see our local guides</a>.</p>'),
 sources=[('Ville de Paris : stationner pendant un déménagement','https://www.paris.fr/en/pages/how-to-park-when-moving-house-in-paris-29754'),('Ville de Paris : demande d’autorisation en ligne','https://teleservices2.paris.fr/demenagements/'),('DRIEAT Île-de-France','https://www.drieat.ile-de-france.developpement-durable.gouv.fr/')]),

dict(key='portugal',slug=('demenager-au-portugal','moving-to-portugal'),theme='etranger',photo='lisbonne',mn=5,svc='europe',
 title=('Déménager au Portugal','Moving to Portugal'),
 lead=('Les démarches avant le départ, le transport de vos biens et les premières formalités sur place.','Paperwork before you leave, transporting your belongings and the first formalities on arrival.'),
 sections=[
  (('Avant de partir','Before you leave'),
   ('<ul><li>Donnez congé, résiliez ou transférez vos contrats, et déclarez votre changement d’adresse.</li><li>Renseignez-vous auprès de votre caisse d’assurance maladie sur votre couverture santé à l’étranger.</li><li>Inscrivez-vous, si vous le souhaitez, au registre des Français établis hors de France : c’est facultatif mais utile pour les démarches consulaires.</li></ul>',
    '<ul><li>Give notice, cancel or transfer your contracts, and report your change of address.</li><li>Check with your health insurance fund how you are covered abroad.</li><li>If you wish, register with the French consular register abroad: optional but useful for consular formalities.</li></ul>')),
  (('Le transport de vos biens','Transporting your belongings'),
   ('<p>Au sein de l’Union européenne, vos biens personnels circulent sans formalité de douane. Un inventaire détaillé reste indispensable : il sert de référence au chargement et à la livraison. Selon le volume, le transport se fait en camion dédié ou en groupage, avec d’autres déménagements sur le même trajet.</p><p>Les centres historiques de Lisbonne et de Porto ont des rues étroites et pentues : l’accès est étudié à l’avance, et la solution est indiquée dans le devis.</p>',
    '<p>Within the European Union, personal belongings move without customs formalities. A detailed inventory is still essential: it is the reference at loading and delivery. Depending on volume, transport is by dedicated truck or by shared load, with other moves on the same route.</p><p>The historic centres of Lisbon and Porto have narrow, steep streets: access is assessed in advance, and the solution is set out in the quote.</p>')),
  (('À l’arrivée','On arrival'),
   ('<ul><li><strong>NIF</strong> : le numéro fiscal portugais, demandé auprès des services des impôts (Finanças). Il est nécessaire pour la plupart des démarches : bail, banque, contrats.</li><li><strong>Certificat d’enregistrement</strong> : au-delà de 3 mois de séjour, les citoyens européens se déclarent à la mairie (Câmara Municipal) de leur lieu de résidence. Le certificat est valable 5 ans.</li></ul>',
    '<ul><li><strong>NIF</strong>: the Portuguese tax number, requested from the tax office (Finanças). It is needed for most formalities: lease, bank, contracts.</li><li><strong>Registration certificate</strong>: after 3 months, EU citizens register with the town hall (Câmara Municipal) where they live. The certificate is valid for 5 years.</li></ul>')),
 ],
 tip=('Notre équipe parle portugais : un vrai plus pour échanger avec le voisinage ou le gardien le jour de la livraison.','Our team speaks Portuguese: a real help when talking to neighbours or the caretaker on delivery day.'),
 faq=[(('Faut-il déclarer ses meubles à la douane ?','Do I need to declare my furniture at customs?'),('Non, entre la France et le Portugal, pays de l’Union européenne, vos biens personnels circulent sans formalité douanière.','No, between France and Portugal, both EU countries, personal belongings move without customs formalities.')),
      (('Qu’est-ce que le groupage ?','What is a shared load?'),('Votre mobilier voyage dans un camion qui transporte plusieurs déménagements sur le même trajet. C’est souvent plus économique pour un volume modéré, avec des dates plus souples.','Your furniture travels in a truck carrying several moves on the same route. It is often more economical for a moderate volume, with more flexible dates.'))],
 sources=[('UFE : s’installer au Portugal','https://ufe.org/dossier-pays/sinstaller-au-portugal/'),('Service-Public : je déménage en France',SP+'F14128')]),

dict(key='espagne',slug=('demenager-en-espagne','moving-to-spain'),theme='etranger',photo='ancien-12',mn=5,svc='europe',
 title=('Déménager en Espagne','Moving to Spain'),
 lead=('Préparer le départ, faire voyager vos biens et accomplir les premières démarches espagnoles.','Preparing to leave, shipping your belongings and completing your first Spanish formalities.'),
 sections=[
  (('Avant de partir','Before you leave'),
   ('<ul><li>Donnez congé, résiliez ou transférez vos contrats, et déclarez votre changement d’adresse.</li><li>Vérifiez votre couverture santé auprès de votre caisse d’assurance maladie.</li><li>Pour vous installer, prévoyez un logement avec un bail ou un titre de propriété : il sera demandé pour vos démarches.</li></ul>',
    '<ul><li>Give notice, cancel or transfer your contracts, and report your change of address.</li><li>Check your health cover with your health insurance fund.</li><li>To settle, plan a home with a lease or title deed: you will need it for your formalities.</li></ul>')),
  (('Le transport de vos biens','Transporting your belongings'),
   ('<p>Entre la France et l’Espagne, pays de l’Union européenne, vos biens personnels circulent sans formalité de douane. L’inventaire détaillé sert de référence au chargement et à la livraison. Selon le volume et vos dates, le transport se fait en camion dédié ou en groupage.</p>',
    '<p>Between France and Spain, both EU countries, personal belongings move without customs formalities. The detailed inventory is the reference at loading and delivery. Depending on volume and dates, transport is by dedicated truck or shared load.</p>')),
  (('À l’arrivée','On arrival'),
   ('<ul><li><strong>Empadronamiento</strong> : l’inscription au registre de la mairie de votre commune, avec votre pièce d’identité et votre bail.</li><li><strong>Certificat d’enregistrement de citoyen de l’Union</strong> : obligatoire au-delà de 3 mois. Il se demande sur rendez-vous (cita previa) auprès des services des étrangers ou de la police, et porte votre numéro d’identification d’étranger, le NIE.</li><li>On vous demandera en général une preuve de ressources et une couverture santé.</li></ul>',
    '<ul><li><strong>Empadronamiento</strong>: registering with your town hall, with your ID and lease.</li><li><strong>EU citizen registration certificate</strong>: compulsory after 3 months. It is requested by appointment (cita previa) at the foreigners’ office or police, and shows your foreigner identification number, the NIE.</li><li>You will usually be asked for proof of means and health cover.</li></ul>')),
 ],
 tip=('Prenez le rendez-vous de la cita previa dès que vous avez votre adresse : les créneaux partent vite dans les grandes villes.','Book your cita previa as soon as you have your address: slots go quickly in big cities.'),
 faq=[(('Le NIE est-il obligatoire ?','Is the NIE compulsory?'),('Pour une installation de plus de 3 mois, oui : il figure sur le certificat d’enregistrement de citoyen de l’Union, et il est demandé pour la plupart des démarches.','For a stay over 3 months, yes: it appears on the EU citizen registration certificate and is needed for most formalities.')),
      (('CODEM parle-t-il espagnol ?','Does CODEM speak Spanish?'),('Oui, notre équipe parle français, anglais, espagnol et portugais.','Yes, our team speaks French, English, Spanish and Portuguese.'))],
 sources=[('Balcells Group : vivre en Espagne en tant que citoyen européen','https://balcellsgroup.com/fr/vivre-en-espagne-citoyen-ue/')]),

dict(key='bureaux',slug=('transfert-de-bureaux','office-relocation'),theme='entreprises',photo='entreprise-hall',mn=5,svc='entreprises',
 title=('Préparer un transfert de bureaux','Planning an office relocation'),
 lead=('Rétroplanning, étiquetage, archives, informatique, formalités : la méthode pour déménager sans arrêter l’activité.','Schedule, labelling, records, IT, formalities: the method for moving without stopping work.'),
 sections=[
  (('Trois mois avant','Three months before'),
   ('<ul><li>Nommez un référent interne, qui sera l’interlocuteur unique du déménageur.</li><li>Organisez une visite des deux sites pour définir les volumes, les accès et les contraintes (ascenseurs, quais, horaires).</li><li>Établissez le plan d’implantation des nouveaux locaux, poste par poste.</li></ul>',
    '<ul><li>Appoint an internal lead, the mover’s single point of contact.</li><li>Arrange a survey of both sites to define volumes, access and constraints (lifts, loading bays, hours).</li><li>Draw up the layout of the new premises, desk by desk.</li></ul>')),
  (('Un mois avant','One month before'),
   ('<ul><li>Triez les archives et les documents : ce qui part, ce qui est détruit, ce qui va en stockage.</li><li>Désignez un relais par service.</li><li>Coordonnez le transfert informatique avec votre prestataire : postes, serveurs, réseau, téléphonie.</li><li>Prévenez clients et fournisseurs de la nouvelle adresse et de la date.</li></ul>',
    '<ul><li>Sort records and documents: what moves, what is destroyed, what goes into storage.</li><li>Appoint a contact in each department.</li><li>Coordinate the IT move with your provider: workstations, servers, network, phones.</li><li>Tell clients and suppliers about the new address and date.</li></ul>')),
  (('L’étiquetage, clé de la réussite','Labelling, the key to success'),
   ('<p>Chaque carton et chaque meuble reçoit une étiquette avec l’étage, le service et le numéro de poste, reporté sur le plan des nouveaux locaux. À l’arrivée, l’équipe dépose tout au bon endroit, sans chercher.</p>',
    '<p>Every box and piece of furniture gets a label with floor, department and desk number, matching the new floor plan. On arrival, the team puts everything in the right place, without searching.</p>')),
  (('Le jour J et la suite','Moving day and after'),
   ('<ul><li>Le transfert peut être organisé en soirée ou le week-end, pour que l’activité continue.</li><li>Le lendemain, faites le tour des postes avec les relais pour régler les derniers détails.</li><li>Pour un transfert de siège social, la formalité se fait en ligne sur le guichet unique des entreprises.</li></ul>',
    '<ul><li>The move can take place in the evening or at the weekend, so work carries on.</li><li>The next day, check every desk with the department contacts to settle final details.</li><li>For a registered office transfer, the formality is done online through the single business registration portal.</li></ul>')),
 ],
 tip=('Un plan d’étage avec un numéro par poste, reporté sur chaque carton : c’est ce qui fait gagner le plus de temps le jour J.','A floor plan with a number per desk, copied onto every box: that is what saves the most time on the day.'),
 faq=[(('Peut-on déménager sans interrompre l’activité ?','Can we move without interrupting work?'),('Oui, en préparant le transfert à l’avance et en l’organisant en soirée ou le week-end.','Yes, by preparing in advance and moving in the evening or at the weekend.')),
      (('Que faire des archives ?','What about our records?'),('Triez-les avant le transfert. Celles à conserver sont transportées dans des cartons archives étiquetés, ou placées en garde-meubles.','Sort them before the move. Those to keep travel in labelled archive boxes, or go into storage.'))],
 sources=[('Guichet unique des formalités d’entreprises','https://formalites.entreprises.gouv.fr/')]),
]
BYKEY={a['key']:a for a in ARTICLES}

def register():
 for a in ARTICLES:
  k='g-'+a['key'];b.routes[k]=(b.routes['conseils'][0]+'/'+a['slug'][0],b.routes['conseils'][1]+'/'+a['slug'][1]);b.labels[k]=a['title']

def _fill(s):
 import re
 s=s.replace('{conseils}',url('conseils'))
 s=re.sub(r'\{g:(\w+)\}',lambda m:url('g-'+m.group(1)),s)
 s=re.sub(r'\{svc:(\w+)\}',lambda m:url(m.group(1)),s)
 if '{prix}' in s:s=s.replace('{prix}',_prix_block())
 return s

def _prix_block():
 from v1content import FORMULES,prix,PRIX_NOTE
 rows=''.join(f'<li><span>{n}</span><strong>{t("dès","from")} {prix(i)}</strong></li>' for i,n in enumerate(FORMULES))
 return f'<ul class="ga-prices">{rows}</ul><p class="ga-note">{t(*PRIX_NOTE)}</p><p><a class="text-link" href="{url("formules")}#tarifs">{t("Comparer les cinq formules","Compare the five packages")}</a></p>'

def card(a,cls=''):
 return f'<a class="gcard {cls}" href="{url("g-"+a["key"])}" data-theme="{a["theme"]}"><div class="image-wrap">{img(a["photo"],t(*a["title"]))}</div><div class="gcard-body"><span class="gtag">{t(*THEMES[a["theme"]])}</span><h3>{t(*a["title"])}</h3><p>{t(*a["lead"])}</p><span class="gmeta">{a["mn"]} min {t("de lecture","read")}</span></div></a>'

def hub():
 chips=f'<button type="button" class="gchip on" data-gfilter="all">{t("Tous","All")}</button>'+''.join(f'<button type="button" class="gchip" data-gfilter="{k}">{t(*v)}</button>' for k,v in THEMES.items())
 return f'<section class="section band-ivory guide-hub" id="guide"><div class="wrap"><div class="section-heading"><div>{eyebrow("Le guide CODEM","The CODEM guide")}<h2>{t("Conseils et astuces<br><em>pour bien déménager.</em>","Tips and advice<br><em>for a smooth move.</em>")}</h2></div><p class="lead">{t("Démarches, emballage, budget, départ à l’étranger : nos guides pratiques, vérifiés et mis à jour.","Paperwork, packing, budget, moving abroad: our practical guides, checked and kept up to date.")}</p></div><div class="gchips" role="group" aria-label="{t("Filtrer par thème","Filter by topic")}">{chips}</div><div class="ggrid">{"".join(card(a) for a in ARTICLES)}</div></div></section>'

def _sid(i):return f's{i+1}'

def article(a):
 secs=a['sections']
 toc=''.join(f'<li><a href="#{_sid(i)}">{t(*h)}</a></li>' for i,(h,_) in enumerate(secs))
 body=''
 for i,(h,c) in enumerate(secs):
  body+=f'<section class="ga-sec" id="{_sid(i)}"><h2>{t(*h)}</h2>{_fill(t(*c))}</section>'
  if i==1:body+=f'<aside class="ga-cta"><div><p class="ga-cta-t">{t("Un projet de déménagement ?","Planning a move?")}</p><p>{t("Devis gratuit et sans engagement, visite offerte, réponse sous 24 h ouvrées.","Free, no-obligation quote, free survey, reply within 1 working day.")}</p></div><div class="actions">{link("devis",t("Demander un devis","Request a quote"),"btn btn-cta")}<a class="text-link" href="{b.PHONE_HREF}">{b.PHONE}</a></div></aside>'
 if a.get('extra'):body+=_fill(t(*a['extra']))
 tip=f'<aside class="ga-tip">{b.mascot("note","ga-tip-mascot",120)}<div><p class="ga-tip-t">{t("L’astuce de Cody","Cody’s tip")}</p><p>{t(*a["tip"])}</p></div></aside>'
 faq=''.join(f'<details><summary>{t(*q)}</summary><p>{t(*r)}</p></details>' for q,r in a['faq'])
 src=''.join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n,u in a['sources'])
 srcs=f'<div class="ga-sources"><p>{t("Sources officielles et références","Official sources and references")}</p><ul>{src}</ul><p class="ga-disclaimer">{t("Informations données à titre indicatif, vérifiées à la date de mise à jour. Les règles peuvent évoluer : consultez la source pour votre situation.","Information given as a guide, checked at the update date. Rules can change: check the source for your situation.")}</p></div>' if a['sources'] else ''
 rel=[x for x in ARTICLES if x['key']!=a['key'] and x['theme']==a['theme']]+[x for x in ARTICLES if x['key']!=a['key'] and x['theme']!=a['theme']]
 related=f'<section class="section band-sand ga-related"><div class="wrap"><div class="section-heading"><div>{eyebrow("À lire aussi","Read next")}<h2>{t("D’autres conseils<br><em>pour votre projet.</em>","More advice<br><em>for your move.</em>")}</h2></div><a class="text-link" href="{url("conseils")}#guide">{t("Tous nos conseils","All our advice")}</a></div><div class="ggrid g3">{"".join(card(x) for x in rel[:3])}</div></div></section>'
 head=f'''<div class="ga-head band-ivory"><div class="wrap ga-head-grid"><div><a class="ga-back" href="{url("conseils")}#guide">← {t("Le guide CODEM","The CODEM guide")}</a><span class="gtag">{t(*THEMES[a["theme"]])}</span><h1>{t(*a["title"])}</h1><p class="lead">{t(*a["lead"])}</p><p class="ga-meta">{a["mn"]} min {t("de lecture","read")} · {t("Mis à jour le","Updated")} {t(*MAJ)}</p></div><div class="image-wrap ga-hero">{img(a["photo"],t(*a["title"]),eager=True)}</div></div></div>'''
 main=f'''<div class="section ga-wrap"><div class="wrap ga-grid"><aside class="ga-toc"><p class="ga-toc-t">{t("Sommaire","Contents")}</p><ol>{toc}<li><a href="#faq">{t("Questions fréquentes","FAQ")}</a></li></ol><div class="ga-toc-box"><p>{t("Besoin d’un conseil personnalisé ?","Need tailored advice?")}</p>{link(a["svc"],cls="text-link")}</div></aside><div class="ga-content">{body}{tip}<section class="ga-sec ga-faq" id="faq"><h2>{t("Questions fréquentes","Frequently asked questions")}</h2>{faq}</section>{srcs}</div></div></div>'''
 return f'<article class="guide-article">{head}{main}</article>'+related+b.cta(t('Votre déménagement,<br><em>bien préparé.</em>','Your move,<br><em>well prepared.</em>'))

def jsonld(a):
 import re
 strip=lambda s:re.sub('<[^>]+>','',s)
 data={"@context":"https://schema.org","@graph":[
  {"@type":"Article","headline":strip(t(*a['title'])),"description":strip(t(*a['lead'])),"dateModified":"2026-10-14","inLanguage":b.LANG,"image":b.SITE_URL+'/assets/'+a['photo']+'-1280.webp',"author":{"@type":"Organization","name":"CODEM Déménagements"},"publisher":{"@type":"Organization","name":"CODEM Déménagements","logo":{"@type":"ImageObject","url":b.SITE_URL+'/assets/logo-codem.png'}},"mainEntityOfPage":b.SITE_URL+url('g-'+a['key'])},
  {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":label('home'),"item":b.SITE_URL+url('home')},{"@type":"ListItem","position":2,"name":label('conseils'),"item":b.SITE_URL+url('conseils')},{"@type":"ListItem","position":3,"name":strip(t(*a['title'])),"item":b.SITE_URL+url('g-'+a['key'])}]},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":t(*q),"acceptedAnswer":{"@type":"Answer","text":t(*r)}} for q,r in a['faq']]}]}
 return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False)+'</script>'

def write_all():
 for a in ARTICLES:
  b.write('g-'+a['key'],article(a),t(*a['lead']),jsonld(a))

register()

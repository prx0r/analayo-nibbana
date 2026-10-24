# Lecture 09 keeps — CF timebase (source 5437.9s / 90.6 min)
# Design notes: forum 0-607.8 cut; second translations cut; big Pali recitations
# split out; dewdrop passage 3594.6-3735.6 unsplittable (CF mid-sentence boundaries)
# so kept whole as one span.

KEEPS = [
    (607.8, 656.0, 1),      # bridge + nibbana motto (Pali chant kept as series signature) + ninth-sermon line
    (728.2, 806.0, 1),      # Satipatthana postures instruction + one-man dumpshaw + form-aspect
    (812.3, 865.8, 1),      # four great primaries / upadaya relativity / Salayatana-vibhanga intro (Pali formula cut)
    (886.6, 908.4, 1),      # hands/feet relativity EN
    (929.2, 952.2, 1),      # no-hands EN + basic principle of relativity
    (1077.2, 1111.3, 2),    # spectator/pantomime emptiness of both
    (1112.1, 1186.7, 1),    # sankhara apt for drama + purpose of impermanence perception + three deliverances
    (1189.8, 1276.9, 1),    # seven suns / Surya Sutta holocaust -> voidness + arahant on hearing
    (1297.7, 1316.5, 1),    # perception-of-impermanence formula EN
    (1365.8, 1374.6, 1),    # impermanence leads to voidness (bridge)
    (1386.4, 1401.4, 1),    # not-self -> destruction of I-am conceit EN quote
    (1425.4, 1438.8, 1),    # assessment + Dhammapada intro
    (1450.2, 1461.2, 1),    # sons/wealth verse EN
    (1476.0, 1534.0, 2),    # sunyata dictum + afraid-of-voidness + sutta prediction
    (1534.0, 1566.7, 1),    # Sutta Nipata intro + Mogha Raja question (covers fragmentary EN in gap)
    (1584.5, 1604.4, 1),    # Mogha Raja answer verse EN
    (1625.2, 1633.3, 1),    # entire Dhamma inclines towards voidness (first sentence)
    (1683.6, 1705.3, 1),    # King Moolaka Sutta intro (Pali question list cut)
    (1727.9, 1767.8, 1),    # nine questions + monks' confession + Buddha's instruction
    (1794.4, 1820.5, 1),    # English answers (rooted in desire ... deliverance as essence)
    (2095.5, 2184.4, 1),    # commentators underestimated questionnaire + Dhammapada first-two application
    (2215.6, 2394.8, 1),    # chanda interpretation chapter + Unnabha dialogue to "described as follows"
    (2418.0, 2447.5, 1),    # four iddhipada EN formula (Pali recitation cut)
    (2479.4, 2576.2, 1),    # Ananda reply + Brahmin objection + park simile + chanda-for-abandonment + middle path
    (2857.7, 2930.1, 1),    # raddhi-for-nibbana + chanda/tanha discretion + mityasati/mityasamadhi
    (2931.6, 3028.2, 2),    # wrong-mindfulness commentarial quote (spoken "Comment" falls in gap)
    (3032.1, 3089.8, 1),    # sequential coherence + rubbish-heap/gem + rooted in desire
    (3099.5, 3131.3, 1),    # origination through attention + mind is forerunner
    (3150.2, 3344.5, 1),    # feeling->concentration->mindfulness->wisdom->deliverance is the essence
    (3516.0, 3562.2, 1),    # goodness of the norm + radical attention + visible-here-now
    (3564.3, 3593.2, 2),    # Brahmins one-stanza arahantship + miracle of Dhamma
    (3594.6, 3735.6, 1),    # rainbow/dewdrop + sammaditta-micchaditta + Samiddhi Sutta intro (unsplittable)
    (3792.9, 3823.7, 1),    # catechism asks about thoughts and concepts
    (3832.8, 3939.4, 1),    # English Samiddhi catechism Q&A
    (3942.9, 4051.0, 1),    # noteworthy points + deathless=nibbana + path through name-and-form
    (4077.2, 4089.1, 1),    # consciousness entangled + Dhammapada verse intro
    (4104.6, 4119.9, 1),    # Dhammapada verse EN (untrammeled by name and form)
    (4143.8, 4159.7, 1),    # path transcends name-and-form + Brahmachala-sutta intro
    (4161.0, 4182.2, 1),    # 62 wrong views lose luster + film-show reference
    (4215.6, 4243.7, 1),    # heretics dogmatically hold name-and-form + Vibhanga parallel
    (4259.0, 4271.6, 1),    # seeing-man verse EN
    (4294.1, 4381.2, 2),    # higher knowledges + tinted-window simile
    (4387.2, 4437.6, 1),    # supramundane vision + Brahma-Jala super-net simile
    (4443.0, 4497.4, 2),    # who casts the net: commentary=Buddha, parallels=Mara
    (4540.3, 4617.9, 1),    # mesh of the net = contact + six bases + Nibbana vision
    (4664.6, 4704.9, 1),    # dependent-origination chain EN + five-aspect knowledge
    (4829.5, 4895.7, 1),    # distinction dogmatists vs vision + light of wisdom (five aspects)
    (4915.0, 4933.3, 1),    # name-form reflected on consciousness + Nidana Samyutta six classes
    (4952.1, 4968.1, 1),    # six consciousnesses EN quote
    (4989.5, 5006.9, 1),    # not a relink consciousness + six sense bases established
    (5009.4, 5080.7, 2),    # internal/external dichotomy -> personality view
    (5082.7, 5198.0, 2),    # Ummaggajataka gem-in-pond parable
    (5199.4, 5363.3, 1),    # via media between two extremes + reflection + shadow + consciousness verse
    (5376.1, 5387.6, 1),    # final verse EN: only they see who have eyes to see
]

MAJOR = [
    (0.0, 607.8, "forum", "course welcome + previous-lecture forum discussion + Robert Baer impermanence preamble"),
    (656.0, 728.2, "recap", "lecture-8 recap of postures and dumpshaw analogy"),
    (952.9, 1003.9, "translation", "Vicakkarani restatement of relativity + Chinese parallel note"),
    (1051.4, 1077.2, "aside", "instructor comment: early suttas not mind-only"),
    (1316.5, 1364.4, "translation", "Bodhi translation of impermanence formula + Chinese parallel + synthesis"),
    (1401.4, 1424.3, "translation", "Bodhi translation of not-self quote + Madhyama Agama parallel"),
    (1461.2, 1476.0, "translation", "K.R. Norman second translation of sons/wealth verse"),
    (1604.4, 1625.2, "translation", "Bhikkhu Bodhi second translation of Mogha Raja verse"),
    (1767.8, 1794.4, "pali", "Pali recitation of King Moolaka answers"),
    (1821.1, 2095.5, "translation", "Bodhi translation of answers + full Madhyama Agama passage + article note + analysis lead-in"),
    (2184.4, 2215.6, "academic", "Peter Skilling comparative study of Dhammapada opening"),
    (2394.8, 2418.0, "pali", "Pali recitation of four iddhipada"),
    (2448.2, 2472.6, "translation", "Bodhi translation of idhhipada formula"),
    (2576.6, 2857.7, "comment", "Western no-desire aside + tanha-nisaya translation comparison (Bodhi/Woodward/Samyukta Agama)"),
    (3344.5, 3516.0, "aside", "meditation-object aside + Bhaddanaga dancing-woman episode + Norman translation"),
    (3735.6, 3792.9, "pali", "Pali recitation of Samiddhi catechism"),
    (3823.7, 3832.8, "aside", "let-us-not-translate remark + gap"),
    (4051.0, 4077.2, "trim", "essence released from name-and-form passage"),
    (4089.1, 4104.6, "pali", "Pali recitation of Dhammapada verse"),
    (4119.9, 4143.8, "translation", "A.K. Norman second translation of Dhammapada verse"),
    (4182.2, 4215.6, "repetition", "re-telling of film-show simile already explained in the series"),
    (4243.7, 4259.0, "pali", "Pali recitation of Vibhanga verse"),
    (4271.6, 4294.1, "translation", "Bodhi second translation of seeing-man verse"),
    (4497.4, 4540.3, "academic", "article citation + forum availability note"),
    (4617.9, 4664.6, "pali", "Pali recitation of dependent-origination chain"),
    (4704.9, 4829.5, "translation", "Walsh translation + Digha Agama insert + recitation remarks + Agama quote"),
    (4933.3, 4952.1, "pali", "Pali recitation of six-consciousnesses passage"),
    (4968.1, 4989.5, "academic", "three Chinese parallels comment"),
    (5363.3, 5376.1, "pali", "Pali recitation of final Itivuttaka verse"),
    (5387.6, 5437.9, "closer", "Ireland second translation + Itivuttaka restatement + instructor closer"),
]

SUMMARY = ("motto -> Satipatthana postures/dumpshaw -> hands/feet relativity -> seven suns -> "
           "impermanence to voidness to not-self -> Dhammapada verses -> King Moolaka catechism -> "
           "chanda/Unnabha iddhipada -> gem-in-rubbish-heap analysis -> Brahmachala 62 views -> "
           "Samiddhi parallel catechism -> via-media/shadow conclusion")

# Roman Pontiffs

265 canonical IDs covering the 267 pontificates of the Holy See's [reference table of Roman Pontiffs](https://www.vatican.va/content/vatican/en/holy-father.html), from Peter to the reigning pope. One row per pontificate, in succession order: `N` is the succession number in the source table, so a pope with multiple pontificates (Benedict IX) repeats his ID. Dates are the source table's strings verbatim — the parsed forms are in [`data/pontiffs.json`](../data/pontiffs.json). Identifiers carry their Roman-numeral ordinal even where the `Papal name` label is bare (`rp:francis-i` — "Francis"): usage attaches "I" to a regnal name only once a later pope takes the same name, and identifiers, unlike labels, must not change when that happens — so the ordinal is minted from the start, `rp:peter` being the sole exception. All IDs are drafts pending committee review ([schema proposal](../docs/schema-proposal.md)).

The `Secular name` column follows the source table's own logic: it is filled only when the pre-election name differs from the papal name — first at n. 56 (John II, born Mercurio, 533, the first pope to change his name) — and for every pope from the eleventh century onward, once taking a regnal name had become the custom and the column also records the family name. A blank therefore means the pope reigned under his own name, not that the name is unknown. Two popes born Pietro — John XIV (n. 136) and Sergius IV (n. 142) — changed their names out of reverence for the Apostle; no pope has ever taken the name Peter. Peter's own secular name, Simon (Mt 16:17; Jn 1:42), is an enrichment beyond the table, which leaves that cell blank — presumably because his renaming was Christ's act, not a regnal-name choice at election. `Country` is the ISO 3166-1 alpha-2 code of the modern country of the place of birth, mapped by the registry from the `Birth` string (blank where the cell names no mappable place or the modern attribution is contested — the mapping policy and per-record notes are in the schema proposal and in `data/pontiffs.json`).

| N | ID | Papal name | Beginning of pontificate | End of pontificate | Secular name | Birth | Country |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rp:peter` | Peter |  | 64 or 67 | Simon | Bethsaida of Galilee |  |
| 2 | `rp:linus-i` | Linus | 68 | 79 |  | Tuscia | IT |
| 3 | `rp:anacletus-i` | Anacletus or Cletus | 80 | 92 |  | Rome | IT |
| 4 | `rp:clement-i` | Clement | 92 | 99 |  | Rome | IT |
| 5 | `rp:evaristus-i` | Evaristus | 99 or 96 | 108 |  | Greece | GR |
| 6 | `rp:alexander-i` | Alexander I | 108 or 109 | 116 or 119 |  | Rome | IT |
| 7 | `rp:sixtus-i` | Sixtus I | 117 or 119 | 126 or 128 |  | Rome | IT |
| 8 | `rp:telesphorus-i` | Telesphorus | 127 or 128 | 137 or 138 |  | Greece | GR |
| 9 | `rp:hyginus-i` | Hyginus | 138 | 142 or 149 |  | Greece | GR |
| 10 | `rp:pius-i` | Pius I | 142 or 146 | 157 or 161 |  | Aquileia | IT |
| 11 | `rp:anicetus-i` | Anicetus | 150 or 157 | 153 or 168 |  | Emesa (Syria) | SY |
| 12 | `rp:soterus-i` | Soterus | 162 or 168 | 170 or 177 |  | Fondi | IT |
| 13 | `rp:eleutherius-i` | Eleutherius | 171 or 177 | 185 or 193 |  | Nicopolis (Epirus) | GR |
| 14 | `rp:victor-i` | Victor I | 186 or 189 | 197 or 201 |  | Africa | TN |
| 15 | `rp:zephyrinus-i` | Zephyrinus | 198 | 217 or 218 |  | Rome | IT |
| 16 | `rp:callistus-i` | Callistus I | 218 | 222 |  | Rome? | IT |
| 17 | `rp:urban-i` | Urban I | 222 | 230 |  | Rome | IT |
| 18 | `rp:pontianus-i` | Pontianus | 21.VII.230 | 28.IX.235 |  | Rome | IT |
| 19 | `rp:anterus-i` | Anterus | 21.XI.235 | 3.I.236 |  | Greece | GR |
| 20 | `rp:fabian-i` | Fabian | ... 236 | 20.I.250 |  | Rome | IT |
| 21 | `rp:cornelius-i` | Cornelius | 6 or 13.III.251 | ... VI.253 |  | Rome | IT |
| 22 | `rp:lucius-i` | Lucius I | ... VI or VII.253 | 5.III.254 |  | Rome | IT |
| 23 | `rp:stephen-i` | Stephen I | 12.III.254 | 2.VIII.257 |  | Rome | IT |
| 24 | `rp:sixtus-ii` | Sixtus II | 30.VIII.257 | 6.VIII.258 |  | Greece | GR |
| 25 | `rp:dionysius-i` | Dionysius | 22.VII.259 | 26.XII.268 |  | Terranova da Sibari (Cosenza)? | IT |
| 26 | `rp:felix-i` | Felix I | 5.I.269 | 30.XII.274 |  | Rome | IT |
| 27 | `rp:eutichianus-i` | Eutichianus | 4.I.275 | 7.XII.283 |  | Luni | IT |
| 28 | `rp:caius-i` | Caius | 17.XII.283 | 22.IV.296 |  | Dalmatia | HR |
| 29 | `rp:marcellinus-i` | Marcellinus | 30.VI.296 | 25.X.304 |  | Rome | IT |
| 30 | `rp:marcellus-i` | Marcellus I | 306 | 16.I.309 |  | Rome | IT |
| 31 | `rp:eusebius-i` | Eusebius | 18.IV.309 | 17.VIII.309 |  | Greece | GR |
| 32 | `rp:miltiades-i` | Miltiades or Melchiades | 2.VII.311 | 10.I.314 |  | Africa | TN |
| 33 | `rp:sylvester-i` | Sylvester I | 31.I.314 | 31.XII.335 |  | Rome | IT |
| 34 | `rp:mark-i` | Mark | 18.I.336 | 7.X.336 |  | Rome | IT |
| 35 | `rp:julius-i` | Julius I | 6.II.337 | 12.IV.352 |  | Rome | IT |
| 36 | `rp:liberius-i` | Liberius | 17.V.352 | 24.IX.366 |  | Romano | IT |
| 37 | `rp:damasus-i` | Damasus I | 1.X.366 | 11.XII.384 |  | Rome | IT |
| 38 | `rp:siricius-i` | Siricius | 15 o 22 o 29.XII.384 | 26.XI.399 |  | Rome | IT |
| 39 | `rp:anastasius-i` | Anastasius I | 27.XI.399 | 19.XII.401 |  | Rome | IT |
| 40 | `rp:innocent-i` | Innocent I | 22.XII.401 | 12.III.417 |  | Albano | IT |
| 41 | `rp:zosimus-i` | Zosimus | 18.III.417 | 26.XII.418 |  | Greece | GR |
| 42 | `rp:boniface-i` | Boniface I | 28,29.XII.418 | 4.IX.422 |  | Rome | IT |
| 43 | `rp:celestine-i` | Celestine I | 10.IX.422 | 27.VII.432 |  | Campania | IT |
| 44 | `rp:sixtus-iii` | Sixtus III | 31.VII.432 | 19.VIII.440 |  | Rome | IT |
| 45 | `rp:leo-i` | Leo I | 29.IX.440 | 10.XI.461 |  | Tuscia | IT |
| 46 | `rp:hilarius-i` | Hilarius | 19.XI.461 | 29.II.468 |  | Sardinia | IT |
| 47 | `rp:simplicius-i` | Simplicius | 3.III.468 | 10.III.483 |  | Tivoli | IT |
| 48 | `rp:felix-iii` | Felix III | 13.III.483 | 25.II o 1.III.492 |  | Rome | IT |
| 49 | `rp:gelasius-i` | Gelasius I | 1.III.492 | 21.XI.496 |  | Africa | TN |
| 50 | `rp:anastasius-ii` | Anastasius II | 24.XI.496 | 19.XI.498 |  | Rome | IT |
| 51 | `rp:symmachus-i` | Symmachus | 22.XI.498 | 19.VII.514 |  | Sardinia | IT |
| 52 | `rp:hormisdas-i` | Hormisdas | 20.VII.514 | 6.VIII.523 |  | Frosinone | IT |
| 53 | `rp:john-i` | John I | 13.VIII.523 | 18.V.526 |  | Tuscia | IT |
| 54 | `rp:felix-iv` | Felix IV | 12.VII.526 | 20 or 22.IX.530 |  | Samnium | IT |
| 55 | `rp:boniface-ii` | Boniface II | 20 o 22.IX.530 | 17.X.532 |  | Rome | IT |
| 56 | `rp:john-ii` | John II | 31.XII.532, 2.I.533 | 8.V.535 | Mercurio | Rome | IT |
| 57 | `rp:agapetus-i` | Agapetus I | 13.V.535 | 22.IV.536 |  | Rome | IT |
| 58 | `rp:silverius-i` | Silverius | 8.VI.536 | ... 537 |  | Frosinone | IT |
| 59 | `rp:vigilius-i` | Vigilius | 29.III.537 | 7.VI.555 |  | Rome | IT |
| 60 | `rp:pelagius-i` | Pelagius I | 16.IV.556 | 4.III.561 |  | Rome | IT |
| 61 | `rp:john-iii` | John III | 17.VII.561 | 13.VII.574 | Catalino | Rome | IT |
| 62 | `rp:benedict-i` | Benedict I | 2.VI.575 | 30.VII.579 |  | Rome | IT |
| 63 | `rp:pelagius-ii` | Pelagius II | 26.XI.579 | 7.II.590 |  | Rome | IT |
| 64 | `rp:gregory-i` | Gregory I | 3.IX.590 | 12.III.604 |  | Rome | IT |
| 65 | `rp:sabinian-i` | Sabinian | ... III, 13.IX.604 | 22.II.606 |  | Blera, Tuscia | IT |
| 66 | `rp:boniface-iii` | Boniface III | 19.II.607 | 10.XI.607 |  | Rome | IT |
| 67 | `rp:boniface-iv` | Boniface IV | 25.VIII.608 | 8.V.615 |  | Marsican territory | IT |
| 68 | `rp:adeodatus-i` | Deusdedit or Adeodatus I | 19.X.615 | 8.XI.618 |  | Rome | IT |
| 69 | `rp:boniface-v` | Boniface V | 23.XII.619 | 23.X.625 |  | Naples | IT |
| 70 | `rp:honorius-i` | Honorius I | 27.X.625 | 12.X.638 |  | Campania | IT |
| 71 | `rp:severinus-i` | Severinus | ... X.638, 28.V.640 | 2.VIII.640 |  | Rome | IT |
| 72 | `rp:john-iv` | John IV | ... VIII, 24.XII.640 | 12.X.642 |  | Dalmatia | HR |
| 73 | `rp:theodore-i` | Theodore I | 12.X, 24.XI.642 | 14.V.649 |  | Jerusalem |  |
| 74 | `rp:martin-i` | Martin I | 5.VII.649 | 16.IX.655 |  | Todi | IT |
| 75 | `rp:eugene-i` | Eugene I | 10.VIII.654 | 2.VI.657 |  | Rome | IT |
| 76 | `rp:vitalian-i` | Vitalian | 30.VII.657 | 27.I.672 |  | Segni | IT |
| 77 | `rp:adeodatus-ii` | Adeodatus II | 11.IV.672 | 16.VI.676 |  | Rome | IT |
| 78 | `rp:donus-i` | Donus | 2.XI.676 | 11.IV.678 |  | Rome | IT |
| 79 | `rp:agatho-i` | Agatho | 27.VI.678 | 10.I.681 |  | Sicily | IT |
| 80 | `rp:leo-ii` | Leo II | ... I.681, 17.VIII.682 | 3.VII.683 |  | Sicily | IT |
| 81 | `rp:benedict-ii` | Benedict II | 26.VI.684 | 8.V.685 |  | Rome | IT |
| 82 | `rp:john-v` | John V | 23.VII.685 | 2.VIII.686 |  | Syria | SY |
| 83 | `rp:conon-i` | Conon | 23.X.686 | 21.IX.687 |  | Unknown |  |
| 84 | `rp:sergius-i` | Sergius I | 15.XII.687 | 7.IX.701 |  | Syria | SY |
| 85 | `rp:john-vi` | John VI | 30.X.701 | 11.I.705 |  | Greece | GR |
| 86 | `rp:john-vii` | John VII | 1.III.705 | 18.X.707 |  | Greece | GR |
| 87 | `rp:sisinnius-i` | Sisinnius | 15.I.708 | 4.II.708 |  | Syria | SY |
| 88 | `rp:constantine-i` | Constantine | 25.III.708 | 9.IV.715 |  | Syria | SY |
| 89 | `rp:gregory-ii` | Gregory II | 19.V.715 | 11.II.731 |  | Rome | IT |
| 90 | `rp:gregory-iii` | Gregory III | 18.III.731 | 28.XI.741 |  | Syria | SY |
| 91 | `rp:zachary-i` | Zachary | 3.XII.741 | 15.III.752 |  | Greece | GR |
| 92 | `rp:stephen-ii` | Stephen II | 26.III.752 | 26.IV.757 |  | Rome | IT |
| 93 | `rp:paul-i` | Paul I | ... IV, 29.V.757 | 28.VI.767 |  | Rome | IT |
| 94 | `rp:stephen-iii` | Stephen III | 1,7.VIII.768 | 24.I.772 |  | Sicily | IT |
| 95 | `rp:adrian-i` | Adrian I | 1,9.II.772 | 25.XII.795 |  | Rome | IT |
| 96 | `rp:leo-iii` | Leo III | 26,27.XII.795 | 12.VI.816 |  | Rome | IT |
| 97 | `rp:stephen-iv` | Stephen IV | 22.VI.816 | 24.I.817 |  | Rome | IT |
| 98 | `rp:paschal-i` | Paschal I | 25.I.817 | ... II-V.824 |  | Rome | IT |
| 99 | `rp:eugene-ii` | Eugene II | ... II-V.824 | ...VIII.827 |  | Rome | IT |
| 100 | `rp:valentine-i` | Valentine | ... VIII.827 | ...IX.827 |  | Rome | IT |
| 101 | `rp:gregory-iv` | Gregory IV | ... IX.827, 29.III.828 | 25.I.844 |  | Rome | IT |
| 102 | `rp:sergius-ii` | Sergius II | 25.I.844 | 27.I.847 |  | Rome | IT |
| 103 | `rp:leo-iv` | Leo IV | ...I,10.V.847 | 17.VII.855 |  | Rome | IT |
| 104 | `rp:benedict-iii` | Benedict III | ...VII, 29.IX.855 | 17.IV.858 |  | Rome | IT |
| 105 | `rp:nicholas-i` | Nicholas I | 24.IV.858 | 13.XI.867 |  | Rome | IT |
| 106 | `rp:adrian-ii` | Adrian II | 14.XII.867 | ...XI or XII.872 |  | Rome | IT |
| 107 | `rp:john-viii` | John VIII | 14.XII.872 | 16.XII.882 |  | Rome | IT |
| 108 | `rp:marinus-i` | Marinus I | ... XII.882 | 15.V.884 |  | Gallese | IT |
| 109 | `rp:adrian-iii` | Adrian III | 17.V.884 | ...VIII or IX.885 |  | Rome | IT |
| 110 | `rp:stephen-v` | Stephen V | ...IX.885 | 14.IX.891 |  | Rome | IT |
| 111 | `rp:formosus-i` | Formosus | 6.X.891 | 4.IV.896 |  | Rome? | IT |
| 112 | `rp:boniface-vi` | Boniface VI | 11.IV.896 | 26.IV.896 |  | Rome | IT |
| 113 | `rp:stephen-vi` | Stephen VI | ...V or VI.896 | ...VII or VIII.897 |  | Rome | IT |
| 114 | `rp:romanus-i` | Romanus | ...VII or VIII.897 | ...XI.897 |  | Gallese | IT |
| 115 | `rp:theodore-ii` | Theodore II | ...XII.897 | ...XII.897 or I.898 |  | Rome | IT |
| 116 | `rp:john-ix` | John IX | ..XII.897 or I.898 | ...I-V.900 |  | Tivoli | IT |
| 117 | `rp:benedict-iv` | Benedict IV | ...I-V.900 | ...VII.903 |  | Rome | IT |
| 118 | `rp:leo-v` | Leo V | ... VII.903 | ... IX.903 |  | Ardea | IT |
| 119 | `rp:sergius-iii` | Sergius III | 29.I.904 | 14.IV.911 |  | Rome | IT |
| 120 | `rp:anastasius-iii` | Anastasius III | ... VI or IX.911 | ... VI or VIII or X.913 |  | Rome | IT |
| 121 | `rp:lando-i` | Lando | ... VII or XI.913 | ... III.914 |  | Sabina | IT |
| 122 | `rp:john-x` | John X | ... III or IV.914 | ... V or VI.928 |  | Tossignano (Imola) | IT |
| 123 | `rp:leo-vi` | Leo VI | ... V or VI.928 | ... XII.928 or I.929 |  | Rome | IT |
| 124 | `rp:stephen-vii` | Stephen VII | ...I.929 | ...II.931 |  | Rome | IT |
| 125 | `rp:john-xi` | John XI | ...III.931 | ...I.936 |  | Rome | IT |
| 126 | `rp:leo-vii` | Leo VII | ...I.936 | 13.VII.939 |  | Rome | IT |
| 127 | `rp:stephen-viii` | Stephen VIII | 14.VII.939 | ... X.942 |  | Rome | IT |
| 128 | `rp:marinus-ii` | Marinus II | 30.X,...XI.942 | ...V.946 |  | Rome | IT |
| 129 | `rp:agapetus-ii` | Agapetus II | 10.V.946 | ...XII.955 |  | Rome | IT |
| 130 | `rp:john-xii` | John XII | 16.XII.955 | 14.V.964 | Ottaviano | Counts of Tusculum | IT |
| 131 | `rp:leo-viii` | Leo VIII | 4,6.XII.963 | ...III.965 |  | Rome | IT |
| 132 | `rp:benedict-v` | Benedict V | ...V.964 | 4.VII.964 or 965 |  | Rome | IT |
| 133 | `rp:john-xiii` | John XIII | 1.X.965 | 6.IX.972 |  | Rome | IT |
| 134 | `rp:benedict-vi` | Benedict VI | ...XII.972, 19.I.973 | ...VII.974 |  | Rome | IT |
| 135 | `rp:benedict-vii` | Benedict VII | ...X.974 | 10.VII.983 |  | Rome | IT |
| 136 | `rp:john-xiv` | John XIV | ...XI or XII.983 | 20.VIII.984 | Pietro | Pavia | IT |
| 137 | `rp:john-xv` | John XV | ...VIII.985 | ...III.996 |  | Rome | IT |
| 138 | `rp:gregory-v` | Gregory V | 3.V.996 | ...II or III.999 | Bruno of Carinthia | Saxony | DE |
| 139 | `rp:sylvester-ii` | Sylvester II | 2.IV.999 | 12.V.1003 | Gerbert | Aquitaine | FR |
| 140 | `rp:john-xvii` | John XVII | 16.V.1003 | 6.XI.1003 | Siccone | Rome | IT |
| 141 | `rp:john-xviii` | John XVIII | 25.XII.1003 | ...VI or VII.1009 | Fasano | Rome | IT |
| 142 | `rp:sergius-iv` | Sergius IV | 31.VII.1009 | 12.V.1012 | Pietro | Rome | IT |
| 143 | `rp:benedict-viii` | Benedict VIII | 18.V.1012 | 9.IV.1024 | Teofilatto dei conti di Tuscolo | Rome? | IT |
| 144 | `rp:john-xix` | John XIX | 19.IV.1024 | ...1032 | Romano dei conti di Tuscolo | Rome? | IT |
| 145 | `rp:benedict-ix` | Benedict IX | ...VIII or IX.1032 | ...IX.1044 | Theophylactus of Tusculum | Rome? | IT |
| 146 | `rp:sylvester-iii` | Sylvester III | 13 or 20.I.1045 | ...III.1045 | Giovanni | Rome | IT |
| 147 | `rp:benedict-ix` | Benedict IX | 10.III.1045 | 1.V.1045 | Theophylactus of Tusculum | Rome? | IT |
| 148 | `rp:gregory-vi` | Gregory VI | 1.V.1045 | 20.XII.1046 | Giovanni Graziano | Rome | IT |
| 149 | `rp:clement-ii` | Clement II | 24.XII.1046 | 9.X.1047 | Suidger, Graf von Morsleben und Hornburg | Saxony | DE |
| 150 | `rp:benedict-ix` | Benedict IX | ...X.1047 | ... VIII.1048 | Theophylactus of Tusculum | Rome? | IT |
| 151 | `rp:damasus-ii` | Damasus II | 17.VII.1048 | 9.VIII.1048 | Poppo | Tyrol | DE |
| 152 | `rp:leo-ix` | Leo IX | 2,12.II.1049 | 19.IV.1054 | Bruno of Eguisheim-Dagsburg | Alsace | FR |
| 153 | `rp:victor-ii` | Victor II | 13.IV.1055 | 28.VII.1057 | Gebhard Of Dollnstein-hirschberg | Swabia | DE |
| 154 | `rp:stephen-ix` | Stephen IX | 2,3.VIII.1057 | 29.III.1058 | Frédéric de Lorraine | Lorraine? | FR |
| 155 | `rp:nicholas-ii` | Nicholas II | ...XII.1058, 24.I.1059 | 27.VII.1061 | Gérard | Bourgogne | FR |
| 156 | `rp:alexander-ii` | Alexander II | 30.IX, 1.X.1061 | 21.IV.1073 | Anselmo | Baggio (Milano) | IT |
| 157 | `rp:gregory-vii` | Gregory VII | 22.IV,30.VI.1073 | 25.V.1085 | Ildebrando | Tuscia | IT |
| 158 | `rp:victor-iii` | Victor III | 24.V.1086, 9.V.1087 | 16.IX.1087 | Dauferio (Desiderio) | Benevento | IT |
| 159 | `rp:urban-ii` | Urban II | 12.III.1088 | 29.VII.1099 | Odo of Lagery | Châtillon-sur-Marne | FR |
| 160 | `rp:paschal-ii` | Paschal II | 13,14.VIII.1099 | 21.I.1118 | Raniero | Bleda or Galeata | IT |
| 161 | `rp:gelasius-ii` | Gelasius II | 24.I,10.III.1118 | 28.I.1119 | Giovanni Caetani | Gaeta | IT |
| 162 | `rp:callixtus-ii` | Callixtus II | 2,9.II.1119 | 13 or 14.XII.1124 | Guy of Burgundy | Quingey | FR |
| 163 | `rp:honorius-ii` | Honorius II | 15,21.XII.1124 | 13 or 14.II.1130 | Lamberto Scannabecchi | Fiagnano (Imola) | IT |
| 164 | `rp:innocent-ii` | Innocent II | 14,23.II.1130 | 24.IX.1143 | Gregorio Papareschi | Rome | IT |
| 165 | `rp:celestine-ii` | Celestine II | 26.IX,3.X.1143 | 8.III.1144 | Guido | Città di Castello | IT |
| 166 | `rp:lucius-ii` | Lucius II | 12.III.1144 | 15.II.1145 | Gerardo | Bologna | IT |
| 167 | `rp:eugene-iii` | Eugene III | 15,18.II.1145 | 8.VII.1153 | Bernardo | Pisa | IT |
| 168 | `rp:anastasius-iv` | Anastasius IV | 12.VII.1153 | 3.XII.1154 | Corrado | Rome | IT |
| 169 | `rp:adrian-iv` | Adrian IV | 4,5.XII.1154 | 1.IX.1159 | Nicholas Breakspear | Abbot's Lagnley (Hertfordshire) | GB |
| 170 | `rp:alexander-iii` | Alexander III | 7,20.IX.1159 | 30.VIII.1181 | Rolando Bandinelli | Siena | IT |
| 171 | `rp:lucius-iii` | Lucius III | 1. 6.IX.1181 | 25.IX.1185 | Ubaldo Allucingoli | Lucca | IT |
| 172 | `rp:urban-iii` | Urban III | 25.XI,1.XII.1185 | 20.X.1187 | Umberto Crivelli | Milan | IT |
| 173 | `rp:gregory-viii` | Gregory VIII | 21.25.X.1187 | 17.XII.1187 | Alberto di Morra | Benevento | IT |
| 174 | `rp:clement-iii` | Clement III | 19,20.XII.1187 | ...III.1191 | Paolo Scolari | Rome | IT |
| 175 | `rp:celestine-iii` | Celestine III | 10,14.IV.1191 | 8.I.1198 | Giacinto Bobone | Rome | IT |
| 176 | `rp:innocent-iii` | Innocent III | 8.I,22.II.1198 | 16.VII.1216 | Lotario dei conti di Segni | Gavignano (Rome) | IT |
| 177 | `rp:honorius-iii` | Honorius III | 18,24.VII.1216 | 18.III.1227 | Cencio | Rome | IT |
| 178 | `rp:gregory-ix` | Gregory IX | 19,21.III.1227 | 22.VIII.1241 | Ugolino di Segni | Anagni | IT |
| 179 | `rp:celestine-iv` | Celestine IV | 25,28.X.1241 | 10.XI.1241 | Goffredo da Castiglione | Milan | IT |
| 180 | `rp:innocent-iv` | Innocent IV | 25,28.VI.1243 | 7.XII.1254 | Sinibaldo Fieschi | Lavagna (Genoa) | IT |
| 181 | `rp:alexander-iv` | Alexander IV | 12,20.XII.1254 | 25.V.1261 | Rinaldo di Jenne | Jenne (Rome) | IT |
| 182 | `rp:urban-iv` | Urban IV | 29.VIII,4.IX.1261 | 2.X.1264 | Jacques Pantaléon | Troyes | FR |
| 183 | `rp:clement-iv` | Clement IV | 5,22.II.1265 | 29.XI.1268 | Gui Foulques | Saint-Gilles (Southern French) | FR |
| 184 | `rp:gregory-x` | Gregory X | 1.IX.1271,27.III.1272 | 10.I.1276 | Tebaldo Visconti | Piacenza | IT |
| 185 | `rp:innocent-v` | Innocent V | 21.I,22.II.1276 | 22.VI.1276 | Pierre De Tarentaise | Savoy | FR |
| 186 | `rp:adrian-v` | Adrian V | 11.VII.1276 | 18.VIII.1276 | Ottobono Fieschi | Genoa | IT |
| 187 | `rp:john-xxi` | John XXI | 16,20.IX.1276 | 20.V.1277 | Pedro Julião or Pedro Hispano | Lisbon | PT |
| 188 | `rp:nicholas-iii` | Nicholas III | 25.XI, 26.XII.1277 | 22.VIII.1280 | Giovanni Gaetano Orsini | Rome | IT |
| 189 | `rp:martin-iv` | Martin IV | 22.II,23.III.1281 | 29.III.1285 | Simon de Brie or of Brion or of Mainpincien | France | FR |
| 190 | `rp:honorius-iv` | Honorius IV | 2.IV, 20.V.1285 | 3.IV.1287 | Giacomo Savelli | Rome | IT |
| 191 | `rp:nicholas-iv` | Nicholas IV | 22.II.1288 | 4.IV.1292 | Girolamo | Lisciano (Ascoli PIceno) | IT |
| 192 | `rp:celestine-v` | Celestine V | 5.VII, 29.VIII.1294 | 13.XII.1294 | Pietro del Morrone | Molise | IT |
| 193 | `rp:boniface-viii` | Boniface VIII | 24.XII.1294, 23.I.1295 | 11.X.1303 | Benedetto Caetani | Anagni | IT |
| 194 | `rp:benedict-xi` | Benedict XI | 22,27.X.1303 | 7.VII.1304 | Niccolò di Boccasio | Treviso | IT |
| 195 | `rp:clement-v` | Clement V | 5.VI, 14.XI.1305 | 20.IV.1314 | Bertrand de Got | Villandraut (Gironde) | FR |
| 196 | `rp:john-xxii` | John XXII | 7.VIII,5.IX.1316 | 4.XII.1334 | Jacques Duèse | Cahors | FR |
| 197 | `rp:benedict-xii` | Benedict XII | 20.XII.1334, 8.I.1335 | 25.IV.1342 | Jacques Fournier | Saverdun (Southern France) | FR |
| 198 | `rp:clement-vi` | Clement VI | 7,19.V.1342 | 6.XII.1352 | Pierre Roger | Maumont (Limousin) | FR |
| 199 | `rp:innocent-vi` | Innocent VI | 18,30.XII.1352 | 12.IX.1362 | Étienne Aubert | Monts (Limousin) | FR |
| 200 | `rp:urban-v` | Urban V | 28.IX,6.XI.1362 | 19.XII.1370 | Guillaume Grimoard | Grizac (Southern France) | FR |
| 201 | `rp:gregory-xi` | Gregory XI | 30.XII.1370, 3.I.1371 | 26.III.1378 | Pierre Roger de Beaufort | Rosiers d'Egletons (Limousin) | FR |
| 202 | `rp:urban-vi` | Urban VI | 8,18.IV.1378 | 15.X.1389 | Bartolomeo Prignano | Naples | IT |
| 203 | `rp:boniface-ix` | Boniface IX | 2,9.XI.1389 | 1.X.1404 | Pietro Tomacelli | Naples | IT |
| 204 | `rp:innocent-vii` | Innocent VII | 17.X,11.XI.1404 | 6.XI.1406 | Cosma Migliorati | Sulmona | IT |
| 205 | `rp:gregory-xii` | Gregory XII | 30.XI,19.XII.1406 | 4.VII.1415 | Angelo Correr | Venice | IT |
| 206 | `rp:martin-v` | Martin V | 11,21.XI.1417 | 20.II.1431 | Oddone Colonna | Genazzano | IT |
| 207 | `rp:eugene-iv` | Eugene IV | 3,11.III.1431 | 23.II.1447 | Gabriele Condulmer | Venice | IT |
| 208 | `rp:nicholas-v` | Nicholas V | 6,19.III.1447 | 24.III.1455 | Tommaso Parentucelli | Sarzana | IT |
| 209 | `rp:callixtus-iii` | Callixtus III | 8,20.IV.1455 | 6.VIII.1458 | Alonso Borja | Torre de Canals, Játiva (Valencia) | ES |
| 210 | `rp:pius-ii` | Pius II | 19.VIII, 3.IX.1458 | 14.VIII.1464 | Enea Silvio Piccolomini | Corsignano (Siena) | IT |
| 211 | `rp:paul-ii` | Paul II | 30.VIII, 16.IX.1464 | 26.VII.1471 | Pietro Barbo | Venice | IT |
| 212 | `rp:sixtus-iv` | Sixtus IV | 1,9,25.VIII.1471 | 12.VIII.1484 | Francesco della Rovere | Celle (Savona) | IT |
| 213 | `rp:innocent-viii` | Innocent VIII | 29.VIII, 12.IX.1484 | 25.VII.1492 | Giovanni Battista Cibo | Genoa | IT |
| 214 | `rp:alexander-vi` | Alexander VI | 11,26.VIII.1492 | 18.VIII.1503 | Rodrigo de Borja | Játiva (Valencia) | ES |
| 215 | `rp:pius-iii` | Pius III | 22.IX, 1,8.X.1503 | 18.X.1503 | Francesco Todeschini-Piccolomini | Siena | IT |
| 216 | `rp:julius-ii` | Julius II | 1,26.XI.1503 | 21.II.1513 | Giuliano della Rovere | Albisola (Savona) | IT |
| 217 | `rp:leo-x` | Leo X | 11,19.III.1513 | 1.XII.1521 | Giovanni de' Medici | Florence | IT |
| 218 | `rp:adrian-vi` | Adrian VI | 9.I,31.VIII.1522 | 14.IX.1523 | Adriaan Florensz | Utrecht | NL |
| 219 | `rp:clement-vii` | Clement VII | 19,26.XI.1523 | 25.IX.1534 | Giulio de' Medici | Florence | IT |
| 220 | `rp:paul-iii` | Paul III | 13.X, 3.XI.1534 | 10.XI.1549 | Alessandro Farnese | Canino (Viterbo) | IT |
| 221 | `rp:julius-iii` | Julius III | 7,22.II.1550 | 23.III.1555 | Giovanni Maria Ciocchi del Monte | Rome | IT |
| 222 | `rp:marcellus-ii` | Marcellus II | 9,10.IV.1555 | 1.V.1555 | Marcello Cervini | Montefano | IT |
| 223 | `rp:paul-iv` | Paul IV | 23,26.V.1555 | 18.VIII.1559 | Gian Pietro Carafa | Capriglia (Avellino) | IT |
| 224 | `rp:pius-iv` | Pius IV | 26.XII.1559, 6.I.1560 | 9.XII.1565 | Giovan Angelo Medici | Milan | IT |
| 225 | `rp:pius-v` | Pius V | 7,17.I.1566 | 1.V.1572 | Antonio (Michele) Ghisleri | Bosco (Alessandria) | IT |
| 226 | `rp:gregory-xiii` | Gregory XIII | 13,25.V.1572 | 10.IV.1585 | Ugo Boncompagni | Bologna | IT |
| 227 | `rp:sixtus-v` | Sixtus V | 24.IV, 1.V.1585 | 27.VIII.1590 | Felice Peretti | Grottammare (Ascoli Piceno) | IT |
| 228 | `rp:urban-vii` | Urban VII | 15.IX.1590 | 27.IX.1590 | Giambattista Castagna | Rome | IT |
| 229 | `rp:gregory-xiv` | Gregory XIV | 5,8.XII.1590 | 16.X.1591 | Niccolò Sfondrati | Somma Lombarda | IT |
| 230 | `rp:innocent-ix` | Innocent IX | 29.X,3.XI.1591 | 30.XII.1591 | Giovan Antonio Facchinetti | Bologna | IT |
| 231 | `rp:clement-viii` | Clement VIII | 30.I,9.II.1592 | 3.III.1605 | Ippolito Aldobrandini | Fano | IT |
| 232 | `rp:leo-xi` | Leo XI | 1,10.IV.1605 | 27.IV.1605 | Alessandro de' Medici | Florence | IT |
| 233 | `rp:paul-v` | Paul V | 16,29.V.1605 | 28.I.1621 | Camillo Borghese | Rome | IT |
| 234 | `rp:gregory-xv` | Gregory XV | 9,14.II.1621 | 8.VII.1623 | Alessandro Ludovisi | Bologna | IT |
| 235 | `rp:urban-viii` | Urban VIII | 6.VIII, 29.IX.1623 | 29.VII.1644 | Maffeo Barberini | Florence | IT |
| 236 | `rp:innocent-x` | Innocent X | 15.IX,4.X.1644 | 7.I.1655 | Giovanni Battista Pamphilj | Rome | IT |
| 237 | `rp:alexander-vii` | Alexander VII | 7,18.IV.1655 | 22.V.1667 | Fabio Chigi | Siena | IT |
| 238 | `rp:clement-ix` | Clement IX | 20,26.VI.1667 | 9.XII.1669 | Giulio Rospigliosi | Pistoia | IT |
| 239 | `rp:clement-x` | Clement X | 29.IV,11.V.1670 | 22.VII.1676 | Emilio Altieri | Rome | IT |
| 240 | `rp:innocent-xi` | Innocent XI | 21.IX, 4.X.1676 | 12.VIII.1689 | Benedetto Odescalchi | Como | IT |
| 241 | `rp:alexander-viii` | Alexander VIII | 6,16.X.1689 | 1.II.1691 | Pietro Ottoboni | Venice | IT |
| 242 | `rp:innocent-xii` | Innocent XII | 12,15.VII.1691 | 27.IX.1700 | Antonio Pignatelli | Spinazzola | IT |
| 243 | `rp:clement-xi` | Clement XI | 23,30.XI, 8.XII.1700 | 19.III.1721 | Giovanni Francesco Albani | Urbino | IT |
| 244 | `rp:innocent-xiii` | Innocent XIII | 8,18.V.1721 | 7.III.1724 | Michelangelo Conti | Poli | IT |
| 245 | `rp:benedict-xiii` | Benedict XIII | 29.V, 4.VI.1724 | 21.II.1730 | Pietro Francesco (Vincenzo Maria) Orsini | Gravina | IT |
| 246 | `rp:clement-xii` | Clement XII | 12,16.VII.1730 | 6.II.1740 | Lorenzo Corsini | Florence | IT |
| 247 | `rp:benedict-xiv` | Benedict XIV | 17,22.VIII.1740 | 3.V.1758 | Prospero Lambertini | Bologna | IT |
| 248 | `rp:clement-xiii` | Clement XIII | 6,16.VII.1758 | 2.II.1769 | Carlo Rezzonico | Venice | IT |
| 249 | `rp:clement-xiv` | Clement XIV | 19,28.V, 4.VI.1769 | 22.IX.1774 | Giovanni Vincenzo Antonio (Lorenzo) Ganganelli | Sant'Arcangelo di Romagna | IT |
| 250 | `rp:pius-vi` | Pius VI | 15,22.II.1775 | 29.VIII.1799 | Giannangelo Braschi | Cesena | IT |
| 251 | `rp:pius-vii` | Pius VII | 14,21.III.1800 | 20.VIII.1823 | Barnaba (Gregorio) Chiaramonti | Cesena | IT |
| 252 | `rp:leo-xii` | Leo XII | 28.IX, 5.X.1823 | 10.II.1829 | Annibale della Genga | Monticelli di Genga (Fabriano) | IT |
| 253 | `rp:pius-viii` | Pius VIII | 31.III, 5.IV.1829 | 30.XI.1830 | Francesco Saverio Castiglioni | Cingoli | IT |
| 254 | `rp:gregory-xvi` | Gregory XVI | 2,6.II.1831 | 1.VI.1846 | Bartolomeo Alberto (Mauro) Cappellari | Belluno | IT |
| 255 | `rp:pius-ix` | Pius IX | 16,21.VI.1846 | 7.II.1878 | Giovanni Maria Mastai Ferretti | Senigallia | IT |
| 256 | `rp:leo-xiii` | Leo XIII | 20.II, 3.III.1878 | 20.VII.1903 | Vincenzo Gioacchino Pecci | Carpineto Romano | IT |
| 257 | `rp:pius-x` | Pius X | 4,9.VIII.1903 | 20.VIII.1914 | Giuseppe Melchiorre Sarto | Riese (Treviso) | IT |
| 258 | `rp:benedict-xv` | Benedict XV | 3,6.IX.1914 | 22.I.1922 | Giacomo della Chiesa | Genoa | IT |
| 259 | `rp:pius-xi` | Pius XI | 6,12.II.1922 | 10.II.1939 | Achille Ratti | Desio (Milan) | IT |
| 260 | `rp:pius-xii` | Pius XII | 2,12.III.1939 | 9.X.1958 | Eugenio Pacelli | Rome | IT |
| 261 | `rp:john-xxiii` | John XXIII | 28.X, 4.XI.1958 | 3.VI.1963 | Angelo Giuseppe Roncalli | Sotto il Monte (Bergamo) | IT |
| 262 | `rp:paul-vi` | Paul VI | 21,30.VI.1963 | 6.VIII.1978 | Giovanni Battista Montini | Concesio (Brescia) | IT |
| 263 | `rp:john-paul-i` | John Paul I | 26.VIII, 3.IX.1978 | 28.IX.1978 | Albino Luciani | Forno di Canale (Belluno) | IT |
| 264 | `rp:john-paul-ii` | John Paul II | 16,22.X.1978 | 2.IV.2005 | Karol Wojtyła | Wadowice (Kraków) | PL |
| 265 | `rp:benedict-xvi` | Benedict XVI | 19,24.IV.2005 | 28.II.2013 | Joseph Ratzinger | Marktl am Inn (Bavaria) | DE |
| 266 | `rp:francis-i` | Francis | 13,19.III.2013 | 21.IV.2025 | Jorge Mario Bergoglio | Buenos Aires (Argentina) | AR |
| 267 | `rp:leo-xiv` | Leo XIV | 8,18.V.2025 |  | Robert Francis Prevost | Chicago | US |

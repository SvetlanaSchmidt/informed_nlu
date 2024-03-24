from translation_labels.translation_class import Translation, TranslationLabel

label_1 = TranslationLabel(name='1 not equivalent',
                               description='The sentences share very little details. There is very little overlap between the sentences.',
        instances=[Translation(source_sentence='Tournament top seeds South Africa started on the right note when they had a comfortable\
                                    26 - 00 win against 5th seeded Zambia.',
                                target_sentence='Los mejores sembrados del torneo Sudáfrica comenzaron con la nota\
                                    correcta cuando tuvieron una cómoda victoria de 26 - 00 contra el 5o crop Zambia.')])

label_2 = TranslationLabel(name='2 almost not equivalent/hardly equivalent/marginally equivalent',
                               description='The sentences are opposite in their polarity. There is changed word order which results\
                               in different meaning. The target sentence misses the salient information. One of the named entities is changed or replaced.',
        instances=[Translation(source_sentence='Anyone planning a visit to a country that could be considered a war zone should get professional training.',
                                target_sentence='Jeder, der einen Besuch in einem Land plant, das als Kriegsgebiet betrachtet werden könnte, sollte eine Berufsausbildung erhalten.')])

label_3 = TranslationLabel(name='3 mostly equivalent',
                           description = 'The minor details, not salient to the meaning can differ.\
                           There are minor verb tense and/or unit of measurement differences.\
                            In general, there are small non conflicting differences in the meaning of two sentences.\
                            There can be omitted non-critical information and not contradictory infomation can be introduced in the target sentence.',
        instances=[Translation(source_sentence='These are sometimes-crowded family beaches with a good range of shops lining the shore.',
                               target_sentence='Diese Strände sind manchmal überfüllt und bieten eine gute Auswahl an Geschäften am Ufer.')])
        
label_4 = TranslationLabel(name='4 near-equivalent',
                           description = 'Although the translation is very close to the source,\
                            there is the different level of formality between sentences.\
                            The target sentence can contain the different ot the source implications,\
                            different emphasis. The sentences can be of different style. The used idioms or methaphors differ.',
        instances=[Translation(source_sentence='Yet, Spanish is also widely used in public transport and other facilities.',
                               target_sentence='Тем не менее испанский язык также широко используется в общественном транспорте и других объектах.')])
        
label_5 = TranslationLabel(name='5 completely equivalent',
                           description = 'There is full equvalence in the meaning and usage expressions.\
                            The target sentence has the same meaning, formality level, style, emphasis, implication, idioms and methaphors.',
        instances=[Translation(source_sentence='Late on Sunday, the United States President Donald Trump, in a statement delivered via\
                                the press secretary, announced US troops would be leaving Syria.',
                               target_sentence='Rabibāra Bēlā nāgāda, mārkina prēsiḍēnṭa ḍōnālḍa\
                                ṭrāmpa prēsa sēkrēṭāri māraphaṯ ēkaṭi baktabyē jānāna mārkina sēnābāhinī siriẏā chēṛē bēriẏē āsabē.')])
from informed_nlu.data_classes.contradiction_types import Contradiction, ContradictionType

antonymity = ContradictionType(name='antonymity',
                               description='A contradiction based on antonymity means, that a contradiction arises\
        between two statements (Premise and Hypothesis), because the hypothesis contains an antonymous word\
        compared to the premise.',
        instances=[Contradiction(premise='Capital punishment is a catalyst for more crime.',
                                 hypothesis='Capital punishment is a deterrent to crime.')])

negation = ContradictionType(name='negation',
                               description='A contradiction based on negation means, that a contradiction arises\
        between two statements (Premise and Hypothesis), that a statement from the premise\
        is negated in the hypothesis, or vice versa',
        instances=[Contradiction(premise='A closely divided Supreme Court said that juries and not judges must impose a death sentence',
                                 hypothesis='The Supreme Court decided that only judges can impose the death sentence.')])

numeric = ContradictionType(name='numeric_mismatch',
                               description='A contradiction based on numeric mismatch means, that a contradiction arises\
        between two statements (Premise and Hypothesis), because there are mismatching number in premise and hypothesis.',
        instances=[Contradiction(premise='The tragedy of the explosion in Qana that killed more than 50 civilians has presented Israel with a dilemma',
                                 hypothesis='An investigation into the strike in Qana found 28 confirmed dead thus far.')])

factive_embedded_verb = ContradictionType(name='factive_embedding_verb',
                                description='Factive contradiction based on the embedding context means that a contradiction arises\
                                    1. from the mismatch in the embedding context of the verb phrase in the Premise and Hypothesis\
                                    creates the contradictory meaning;\
                                    2. contains similar or identical entities in the Premise and Hypothesis;\
                                    3. Hypothesis does not contain any negations and any antonyms of the verb phrase of the Premise.',
        instances=[Contradiction(premise='Sudan accepted U.N. troops in Darfur.',
                                hypothesis='Sudan refused to accept U.N. troops.'),
                    ])

factive_antonym = ContradictionType(name='factive_antonymity_based',
                                description='Factive contradiction based on the antonymity of a verb means that a contradiction arises\
        between two statements (Premise and Hypothesis), because the verb phrase in Hypothesis has an opposite or contradictory meaning\
        compared to the verb phrase in the Premise.',
        instances=[Contradiction(premise='Sudan refused to allow U.N. troops in Darfur.',
                                 hypothesis='Sudan will grant permission for United Nations peacekeeping forces to take up station in Darfur.')])
        

structure = ContradictionType(name='structure',
                            description='Structure contradiction based on the mismatch in the sentence structure arises\
         from the mismatch in the sentence structure of the premise and hypothesis. The mismatch in the sentnece structure has folowing characteristics:\
        0. the Premise contains the verb or verb phrase\
        1. the created Hypothesis has the same verb phrase as the Premise,\
        2. there are new entities which function as new objects of the same verb in the hypothesis,\
        which creates the contradictory meaning to the meaning of the premise with respect to premise',
        instances=[Contradiction(premise='The children are smiling and waving at the camera.',
                                 hypothesis='The children are smiling and waving to each other.')])

lexical = ContradictionType(name='lexical',
                            description='Lexical contradiction based on the mismatch in the lexical context has following characteristics:\
        0. the Premise and Hypothesis has both the same topic or verb subject\
        1. the created Hypothesis has subtly different lexical meaning\
        2. the Hypothesis has a contradictory meaning due to the created opposite context of the topic in the premise',
        instances=[Contradiction(premise='Tariq Aziz kept outside the closed circle of Saddam s Sunni Moslem cronies.',
                                 hypothesis='Tariq Aziz was in Saddam s inner circle.')])

wk = ContradictionType(name='WorldKnowledge',
                            description='Lexical contradiction based on the mismatch in world knowledge has following characteristics:\
        0. the Premise contains the well known knowledge about the world\
        1. the facts and knowledge from the Hypothesis contradict to the world knowledge in the Premise',
        instances=[Contradiction(premise='Al-zarqawi was Palestinian.',
                                 hypothesis='Al-zarqawi was Jordanian.')])

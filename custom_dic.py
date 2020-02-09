
from nltk.corpus import wordnet



arg_words = ['teaching', 'impossible', 'order', 'extreme', 'nurse', 'living', 'background', 'outcome', 'discourages', 'worker', 'apprenticeship', 'aimed', 'sufficient', 'countermeasure', 'affluent', 'performance', 'understand', 'hanging', 'pushed', 'investment', 'trained', 'youth', 'system', 'family', 'effort', 'accessible', 'horizon', 'successful', 'grade', 'human', 'house', 'interest', 'readily', 'economy', 'fully', 'people', 'requires', 'worrying', 'solicitor', 'future', 'necessarily', 'studying', 'selective', 'prestige', 'inclined', 'applied', 'complete', 'struggling', 'rich', 'stem', 'opportunity', 'decide', 'weight', 'achieving', 'drive', 'adjust', 'decent', 'desire', 'external', 'scheme', 'poorer', 'typically', 'stop', 'increase', 'significant', 'result', 'encourage', 'completing', 'quality', 'group', 'main', 'guarantee', 'barely', 'earnings', 'start', 'enjoyable', 'post', 'accessed', 'finance', 'workforce', 'highly', 'study', 'meet', 'asked', 'expand', 'borrowed', 'attend', 'employment', 'applying', 'based', 'demeaning', 'defaulting', 'worthy', 'barrier', 'important', 'pay', 'mistake', 'backing', 'idea', 'shift', 'repaid', 'misspend', 'finish', 'placing', 'confidence', 'teacher', 'include', 'qualified', 'today', 'part', 'built', 'possibly', 'prospect', 'ability', 'great', 'competition', 'health', 'type', 'end', 'day', 'entry', 'knowing', 'begin', 'teenager', 'treat', 'fight', 'graduate', 'measure', 'completely', 'thought', 'reasonable', 'choice', 'adult', 'poor', 'juggle', 'demand', 'incremental', 'spend', 'loaned', 'ambition', 'abolished', 'student', 'fast', 'graduating', 'limit', 'potential', 'starting', 'past', 'advice', 'enrich', 'place', 'struggle', 'ha', 'smaller', 'infinite', 'scholarship', 'diversity', 'usa', 'written', 'boycotting', 'employing', 'criterion', 'fear', 'wiped', 'country', 'impact', 'young', 'talked', 'fee', 'earned', 'afraid', 'child', 'efficiently', 'good', 'injustice', 'inequality', 'equal', 'year', 'isn', 'enter', 'sustainable', 'prospective', 'taking', 'immediately', 'cut', 'vast', 'essential', 'debt', 'lower', 'simply', 'rate', 'provider', 'pursuing', 'effect', 'excessive', 'life', 'underprivileged', 'graduated', 'assistance', 'paying', 'finding', 'industry', 'thrive', 'percentage', 'goal', 'hard', 'ending', 'offer', 'needed', 'hardship', 'stand', 'high', 'problem', 'cared', 'large', 'bettered', 'profit', 'apply', 'like', 'pressure', 'return', 'rising', 'financial', 'cover', 'deliberately', 'employer', 'degree', 'basically', 'bad', 'testing', 'issue', 'application', 'entire', 'affair', 'service', 'bachelor', 'tight', 'university', 'lot', 'portion', 'big', 'privileged', 'find', 'doctor', 'workplace', 'naive', 'unable', 'mention', 'side', 'academic', 'society', 'excellent', 'board', 'subject', 'firstly', 'bring', 'added', 'repay', 'generally', 'area', 'train', 'identified', 'miss', 'capacity', 'funding', 'support', 'consumer', 'bursary', 'full', 'charged', 'repaying', 'expendable', 'grant', 'fortunate', 'avenue', 'dropped', 'doe', 'wage', 'made', 'deal', 'devalue', 'hope', 'poorly', 'parent', 'assisted', 'fact', 'opt', 'agree', 'raise', 'wasting', 'unfair', 'owe', 'earn', 'resource', 'risk', 'specialised', 'accepting', 'lead', 'dependant', 'graduation', 'uni', 'contributing', 'job', 'skillsets', 'educated', 'didn', 'mental', 'earning', 'provided', 'arm', 'personal', 'project', 'scrapped', 'access', 'complains', 'individual', 'income', 'directly', 'treated', 'force', 'career', 'tuition', 'perspective', 'live', 'hand', 'subsidise', 'cost', 'discouraged', 'contribute', 'huge', 'time', 'repayment', 'neediest', 'score', 'sadly', 'situation', 'burden', 'long', 'nursing', 'funded', 'competing', 'capable', 'wa', 'relying', 'desirable', 'responsibility', 'counterpart', 'expected', 'ridiculous', 'construction', 'financially', 'manage', 'correct', 'scotland', 'initially', 'accumulates', 'lifelong', 'aren', 'produce', 'skill', 'police', 'whilst', 'level', 'position', 'experience', 'rest', 'doesn', 'driven', 'thing', 'higher', 'playing', 'exploiting', 'gain', 'payer', 'paid', 'education', 'avoid', 'condition', 'restricted', 'maintain', 'stature', 'move', 'mind', 'focus', 'world', 'person', 'hire', 'loan', 'kid', 'tax', 'benefit', 'widely', 'consequence', 'amount', 'success', 'expense', 'achieve', 'undeniable', 'parental', 'form', 'limited', 'burdening', 'exceptional', 'tertiary', 'government', 'viable', 'knowledge', 'city', 'master', 'working', 'monthly', 'rarely', 'affect', 'survive', 'haven', 'afford', 'specialized', 'sort', 'enticing', 'making', 'legal', 'slightly', 'preventative', 'engineer', 'drop', 'spent', 'rent', 'divide', 'dent', 'cheaper', 'saving', 'credit', 'fund', 'slip', 'free', 'salary', 'uk', 'putting', 'invest', 'work', 'adulthood', 'similar', 'option', 'term', 'learn', 'insignificant', 'medic', 'plenty', 'back', 'saddle', 'heavy', 'continue', 'money', 'vein', 'reached', 'travel', 'deprive', 'economic', 'differently', 'chance', 'accepted', 'extortionate', 'age', 'ppl', 'won', 'ethic', 'field', 'population', 'quickly', 'fullness', 'perform', 'maintenance', 'filled', 'steep', 'basic', 'run', 'depends', 'deter', 'multiple', 'germany', 'recently', 'social', 'civilisation', 'circumstance', 'fair', 'low', 'hurting', 'difficult']


arg_words_30 = arg_words[30:60]

all_syns = []

for word in arg_words:
    #print(word)
    synonyms = []
    for syn in wordnet.synsets(word):
    	for l in syn.lemmas():
    		synonyms.append(l.name())
    synonyms = list(set(synonyms))
    syn_3 = synonyms[:3]
    all_syns.extend(syn_3)

print(len(all_syns))

import pickle

with open('glovedic.pickle', 'rb') as handle:
    model_glove = pickle.load(handle)
print(len(model_glove))
#print(argument_words)

print(all_syns)

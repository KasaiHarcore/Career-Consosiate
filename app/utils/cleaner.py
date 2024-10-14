import nltk
from string import punctuation
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import re

class ResumeCleaner:
    """
    ResumeCleaner class is used to clean and preprocess resume data.
    """
    def __init__(self, data):
        # Initializing the stopwords, punctuations, and lemmatizer
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')

        self.stopwords = set(stopwords.words('english'))
        self.punctuations = set(punctuation)
        self.lemmatizer = WordNetLemmatizer()
        

        data = self.format_category(data)
        data = self.format_columns(data)
        
        data["cleaned_resume"] = data["resume"].apply(self.clean_function)
        data["cleaned_resume"] = data["cleaned_resume"].apply(self.preprocess)
        
        data = self.data_checking(data)
        self.data = data

    def get_data(self):
        return self.data

    def get_wordnet_pos(self, tag: str) -> str:
        """
        Convert POS tag to a format recognized by the lemmatizer.
        """
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def format_category(self, data):
        """
        Clean the 'Category' column by converting it to lowercase and replacing spaces or hyphens.
        """
        data['Category'] = data['Category'].apply(lambda x: x.lower().replace(' ', '_').replace('-', '_'))
        return data
    
    def format_columns(self, data):
        """
        Format the column names by converting them to lowercase and replacing spaces with underscores.
        """
        data.columns = data.columns.str.lower().str.replace(' ', '_')
        return data

    def clean_function(self, resumeText):
        """
        Clean the resume text by removing URLs, mentions, hashtags, punctuations, and non-ASCII characters.
        """
        resumeText = re.sub(r'http\S+\s*', ' ', resumeText)  # remove URLs
        resumeText = re.sub(r'RT|cc', ' ', resumeText)  # remove RT and cc
        resumeText = re.sub(r'#\S+', '', resumeText)  # remove hashtags
        resumeText = re.sub(r'@\S+', '  ', resumeText)  # remove mentions
        resumeText = re.sub(f"[{re.escape(punctuation)}]", ' ', resumeText)  # remove punctuations
        resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)  # remove non-ASCII characters
        resumeText = re.sub(r'\s+', ' ', resumeText)  # replace multiple spaces with single space
        return resumeText

    def preprocess(self, text):         
        """
        Preprocess the cleaned text: tokenize, remove stopwords, lemmatize using POS tagging.
        """
        # Lowercase
        text = text.lower()
        
        # Tokenize text
        words = nltk.word_tokenize(text)
        
        # Remove stopwords and punctuations
        words = [word for word in words if word not in self.stopwords and word not in self.punctuations]
        
        # POS tagging
        pos_tags = nltk.pos_tag(words)
        
        # Lemmatize with POS tagging
        lemmatized_words = [self.lemmatizer.lemmatize(word, self.get_wordnet_pos(tag)) for word, tag in pos_tags]
        
        return ' '.join(lemmatized_words)

    def data_checking(self, data):
        """
        Check for duplicate resumes in the 'cleaned_resume' column and remove them.
        """
        if data["cleaned_resume"].duplicated().sum() > 0:
            data = data.drop_duplicates(subset="cleaned_resume", keep="first")
        else:
            print("No duplicate resumes found.")
        return data
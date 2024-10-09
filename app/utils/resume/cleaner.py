import pandas as pd
import numpy as np
import nltk
from string import punctuation
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import re

class ResumeCleaner:
    """
    A class used to clean whole dataset, preparing it for further work.

    Attributes:
    -----------
    data : pd.DataFrame
    

    Methods:
    --------
    expand_abbreviations(text: str) -> str
        Expand abbreviations in the text.
    
    get_wordnet_pos(tag: str) -> str
        Get WordNet POS tag.
        
    format_category(data: pd.DataFrame) -> pd.DataFrame
        Format the category column.
        
    clean_function(resumeText: str) -> str
        Clean the resume text.
        
    preprocess(text: str) -> str
        Preprocess the text.
        
    data_checking(data: pd.DataFrame) -> pd.DataFrame
        Check for duplicate resumes.
        
    get_data() -> pd.DataFrame
        Return the cleaned data.
    """

    def __init__(self, data):
        self.stopwords = set(stopwords.words('english'))
        self.punctuations = set(punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.abbreviation_map = {
                                "i'm": "i am",
                                "you're": "you are",
                                "he's": "he is",
                                "she's": "she is",
                                "it's": "it is",
                                "we're": "we are",
                                "they're": "they are",
                                "isn't": "is not",
                                "aren't": "are not",
                                "wasn't": "was not",
                                "weren't": "were not",
                                "can't": "cannot",
                                "couldn't": "could not",
                                "won't": "will not",
                                "wouldn't": "would not",
                                "don't": "do not",
                                "doesn't": "does not",
                                "didn't": "did not",
                                "hasn't": "has not",
                                "haven't": "have not",
                                "hadn't": "had not"}
        
        # Processing map
        data = self.format_category(data)
        data = self.data_checking(data)
        data["cleaned_resume"] = data["resume"].apply(self.clean_function)
        data["preprocessed_resume"] = data["cleaned_resume"].apply(self.preprocess)
        self.data = data
        
    def get_data(self):
        return self.data
        
    def expand_abbreviations(self, text):
        for abbr, full_form in self.abbreviation_map.items():
            text = re.sub(r'\b' + abbr + r'\b', full_form, text)
        return text
    
    def get_wordnet_pos(self, tag: str) -> str:
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
        data['Category'] = data['category'].apply(lambda x: x.lower().replace(' ', '_').replace('-', '_'))
        return data
    
    def clean_function(self, resumeText):
        resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
        resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
        resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
        resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
        resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
        resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
        resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
        return resumeText
    
    def preprocess(self, text):        
        # Expand abbreviations
        text = self.expand_abbreviations(text)
        
        # Lowercase
        text = text.lower()
        
        # Remove stopwords and punctuations
        words = text.split()
        words = [word for word in words if word not in self.stopwords and word not in self.punctuations]
        text = ' '.join(words)
                
        # Tokenize
        words = nltk.word_tokenize(text)
        
        # Lemmatize
        lemmatizer = WordNetLemmatizer()
        pos_tags = nltk.pos_tag(words)
        
        # Lemmatize with POS tagging
        lemmatized_words = [lemmatizer.lemmatize(word, self.get_wordnet_pos(tag)) for word, tag in pos_tags]
        
        return ' '.join(lemmatized_words)
    
    def data_checking(self, data):
        if data["cleaned_resume"].duplicate().sum() > 0:
            data = data.drop_duplicates(subset = "cleaned_resume", keep = "first")
        else:
            print("No duplicate resumes found.")
        return data
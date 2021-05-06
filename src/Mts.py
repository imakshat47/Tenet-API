import googletrans
from googletrans import Translator
from google_trans_new import google_translator
from textblob import TextBlob
from translate import Translator as trans
import goslate


class MTS(object):

    def __init__(self):
        # translator Initiated
        self.__translator = Translator()
        self.__google_translator = google_translator()

    def _translator(self, _text = None, _lang="en"):
        if _text == None:
            return None
        
        try:
            _translated = self.__translator.translate(_text, dest=_lang)
            _translated = self.__translator.translate(_text, dest="en")
            _text = _translated.text
        except:
            try:
                _text = self.__google_translator.translate(
                    _text, lang_tgt=_lang)
                _text = self.__google_translator.translate(
                    _text, lang_tgt="en")
            except:
                try:
                    _gs = goslate.Goslate()                    
                    _text = _gs.translate(_text, 'en')
                except:
                    _translator = trans(to_lang="en")
                    _text = _translator.translate(_text)

        txtBlob = TextBlob(_text)
        _text = str(txtBlob.correct())
        try:
            _text = str(txtBlob.translate(to='en'))    
        except:
            _text = _text
        return _text

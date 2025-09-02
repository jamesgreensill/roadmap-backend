class PluralEngine:
    # https://www.teachstarter.com/au/teaching-resource/rules-for-plurals-s-es-ies-ves/
    @staticmethod
    def pluralize(noun: str) -> str:
        """
        Convert a singular noun to its plural form based on common English rules.
        """
        if noun.endswith(('ch', 'sh', 's', 'ss', 'x', 'z')):
            return noun + 'es'
        elif noun.endswith('y') and len(noun) > 1 and noun[-2].lower() not in 'aeiou':
            return noun[:-1] + 'ies'
        elif noun.endswith(('f', 'fe')):
            if noun.endswith('fe'):
                return noun[:-2] + 'ves'
            else:
                return noun[:-1] + 'ves'
        else:
            return noun + 's'

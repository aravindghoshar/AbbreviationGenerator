import re

class AbbGen:
    position_values = {1: 1, 2: 2, 3: 3}
    letter_values = {'Q': 1, 'Z': 1, 'J': 3, 'X': 3, 'K': 6, 'F': 7, 'H': 7, 'V': 7, 'W': 7, 'Y': 7,
                     'B': 8, 'C': 8, 'M': 8, 'P': 8, 'D': 9, 'G': 9, 'L': 15, 'N': 15, 'R': 15, 'S': 15,
                     'T': 15, 'O': 20, 'U': 20, 'A': 25, 'I': 25, 'E': 35}

    #Method for cleaning the input data 
    def clean(input_filename):
        with open(input_filename, 'r') as file:
            words = [line.strip('\n') for line in file]

        pattern = re.compile(r"[^a-zA-Z']+")
        cleaned_words = [pattern.sub(' ', word.replace("'", "")) for word in words]
        return cleaned_words

    #Method to generate abbreviations
    def generate_abbreviations(cleaned_word):
        abbr_list = []
        first_letter = cleaned_word[0]
        for i in range(1,len(cleaned_word)):
            if cleaned_word[i] != ' ':
                second_letter = cleaned_word[i]
            else:
                continue
            for j in range(i+1,len(cleaned_word)):
                if cleaned_word[j] != ' ':
                    third_letter = cleaned_word[j]
                    abbr = (first_letter+second_letter+third_letter)
                    abbr = abbr.upper()
                    abbr_list.append(abbr) 
                else:
                    continue 
        filtered_list = list(set(abbr_list))  
        return filtered_list

    #Method to calculate the score
    def calculate_score_for_abbreviation(word, abbr):
        scores = []

        # Split the word into individual words
        words = word.split()

        # Case 1: Single word
        if len(words) == 1:
            for i in range(1, len(abbr)):
                if i - 1 < len(words):  # Check to prevent IndexError
                    letter = abbr[i - 1]
                    scores.append(AbbGen.position_values.get(i, 3) + AbbGen.letter_values.get(letter, 0))

        # Case 2: Two or more words
        else:
            for i in range(1, len(abbr)):
                if i - 1 < len(words):  # Check to prevent IndexError
                    letter = abbr[i - 1]
                    scores.append(AbbGen.position_values.get(i, 3) + AbbGen.letter_values.get(letter, 0))

        return sum(scores)

    #Method to remove duplicates
    def remove_duplicate_abbreviations(word, abbreviations, dict_abbreviations):
        for other_word, other_abbreviations in dict_abbreviations.items():
            if other_word != word:
                common_abbreviations = set(abbreviations) & set(other_abbreviations)
                for common_abbr in common_abbreviations:
                    abbrev_score = AbbGen.calculate_score_for_abbreviation(word, common_abbr)
                    other_score = AbbGen.calculate_score_for_abbreviation(other_word, common_abbr)

                    if abbrev_score <= other_score:
                        abbreviations.remove(common_abbr)

    #Method to calculate the score
    def calculate_score(dict_abbreviations):
        scored_abbreviations = {}

        for word, abbreviations in dict_abbreviations.items():
            min_score = float('inf')
            chosen_abbr = ""

            for abbr in abbreviations:
                score = AbbGen.calculate_score_for_abbreviation(word, abbr)

                if score < min_score:
                    min_score = score
                    chosen_abbr = abbr

            AbbGen.remove_duplicate_abbreviations(word, [chosen_abbr], dict_abbreviations)

            scored_abbreviations[word] = [chosen_abbr]

        return scored_abbreviations

    
    def main():
        input_name = "trees.txt"
        cleaned_words = AbbGen.clean(input_name)

        dict_abbreviations = {}
        for word in cleaned_words:
            abbr_list = AbbGen.generate_abbreviations(word)
            filtered_list = list(set(abbr_list))
            dict_abbreviations[word] = filtered_list

        scored_abbreviations = AbbGen.calculate_score(dict_abbreviations)

        output_filename = f'{input_name.split(".")[0]}_abbrevs.txt'
        with open(output_filename, 'w') as output_file:
            for word, abbreviations in scored_abbreviations.items():
                output_file.write(word + '\n' + abbreviations[0] + '\n' if abbreviations else word + '\n')

        print(f"Results written to {output_filename}")

if __name__ == "__main__":
    AbbGen.main()

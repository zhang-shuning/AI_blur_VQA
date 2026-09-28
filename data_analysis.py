import pathlib
import ast

DATA_FOLDER_PATH = pathlib.Path("data")
IMAGE_AMOUNT = 925

#Dict with all the possible correct answers for each species
#Ai was used to determine whether a specific species name outputted by the ai is correct or not
correct_answers = {
    'abyssinian':('abyssinian'),
    'american_bulldog':('american bulldog'),
    'american_pit_bull_terrier':('pitbull terrier', 'pit bull terrier', 'dog pitbull'),
    'basset_hound':('basset hound'),
    'beagle':('beagle'),
    'bengal':('bengal'),
    'birman':('birman'),
    'bombay':('bombay'),
    'boxer':('boxer'),
    'british_shorthair':('british shorthair'),
    'chihuahua':('chihuahua'),
    'egyptian_mau':('egyptian mau'),
    'english_cocker_spaniel':('english cocker spaniel', 'cocker spaniel'),
    'english_setter':('english setter'),
    'german_shorthaired':('german shorthaired pointer', 'dog german shorthand pointer'),
    'great_pyrenees':('great pyrenees', 'pyrenean mountain dog'),
    'havanese':('havanese'),
    'japanese_chin':('japanese chin'),
    'keeshond':('keeshond'),
    'leonberger':('leonberger'),
    'maine_coon':('maine coon'),
    'miniature_pinscher':('miniature pinscher','minpin','min pin','miniatue pinscher','mincher'),
    'newfoundland':('newfoundland'),
    'persian':('persian'),
    'pomeranian':('pomeranian'),
    'pug':('pug'),
    'ragdoll':('ragdoll'),
    'russian_blue':('russian blue'),
    'saint_bernard':('saint bernard', 'st. bernard'),
    'samoyed':('samoyed'),
    'scottish_terrier':('scottish terrier'),
    'shiba_inu':('shiba inu'),
    'siamese':('siamese'),
    'sphynx':('sphynx'),
    'staffordshire_bull_terrier':('staffordshire bull terrier'),
    'wheaten_terrier':('soft-coated wheaten terrier', 'soft coated wheaten terrier', 'wheaten terrier'),
    'yorkshire_terrier':('yorkshire terrier')
}

#This dictionary was AI generated
breed_species = {
    'abyssinian': 'cat',
    'american_bulldog': 'dog',
    'american_pit_bull_terrier': 'dog',
    'basset_hound': 'dog',
    'beagle': 'dog',
    'bengal': 'cat',
    'birman': 'cat',
    'bombay': 'cat',
    'boxer': 'dog',
    'british_shorthair': 'cat',
    'chihuahua': 'dog',
    'egyptian_mau': 'cat',
    'english_cocker_spaniel': 'dog',
    'english_setter': 'dog',
    'german_shorthaired': 'dog',
    'great_pyrenees': 'dog',
    'havanese': 'dog',
    'japanese_chin': 'dog',
    'keeshond': 'dog',
    'leonberger': 'dog',
    'maine_coon': 'cat',
    'miniature_pinscher': 'dog',
    'newfoundland': 'dog',
    'persian': 'cat',
    'pomeranian': 'dog',
    'pug': 'dog',
    'ragdoll': 'cat',
    'russian_blue': 'cat',
    'saint_bernard': 'dog',
    'samoyed': 'dog',
    'scottish_terrier': 'dog',
    'shiba_inu': 'dog',
    'siamese': 'cat',
    'sphynx': 'cat',
    'staffordshire_bull_terrier': 'dog',
    'wheaten_terrier': 'dog',
    'yorkshire_terrier': 'dog'
}

def get_path_from_result_number(num):
    return DATA_FOLDER_PATH/f"result{num}.txt"

def analyze(path):
    species_correct_dict = {x:0 for x in breed_species}
    breed_correct_dict = {x:0 for x in breed_species}
    species_correct_count = 0
    breed_correct_count = 0
    unknown_species_count = 0
    unknown_breed_count = 0
    with open(path, 'r') as f:
        lines = f.readlines()
    print(lines[0])

    blur_amount = ""
    for i in lines[0]:
        if i.isdigit():
            blur_amount = blur_amount + i

    for i in lines:
        if i[0] != '(': #Checks if it's the first line
            continue
        current_line_tuple:tuple[int,str,str] = ast.literal_eval(i)
        current_breed = current_line_tuple[1]
        ai_full_answer = current_line_tuple[2].replace('_', ' ').replace('-', ' ')
        ai_first_space = ai_full_answer.find(' ')
        ai_species = ai_full_answer[:ai_first_space]
        ai_breed = ai_full_answer[ai_first_space+1:]
        if ai_species == breed_species[current_breed]:
            species_correct_count += 1
            species_correct_dict[current_breed] += 1
        elif ai_species == 'unknown':
            unknown_species_count += 1
        if ai_breed in correct_answers[current_breed]:
            breed_correct_count += 1
            breed_correct_dict[current_breed] += 1
        elif ai_breed == 'unknown':
            unknown_breed_count += 1

    analysis_file_path = pathlib.Path(f'analysis/blur{blur_amount}.txt')
    if analysis_file_path.exists():
        analysis_file_path.unlink()

    with open(analysis_file_path, 'a') as f:
        f.write(f"Blur: {blur_amount}\n")
        f.write(f"Correct species: {species_correct_count}/{IMAGE_AMOUNT}\n")
        f.write(f"Correct breed: {breed_correct_count}/{IMAGE_AMOUNT}\n")
        f.write(f"Unknown species: {unknown_species_count}/{IMAGE_AMOUNT}\n")
        f.write(f"Unknown breed: {unknown_breed_count}/{IMAGE_AMOUNT}\n")
        f.write(f"Correct species dict: {species_correct_dict}\n")
        f.write(f"Correct breed dict: {breed_correct_dict}")

    print(f"{species_correct_count/IMAGE_AMOUNT*100:.2f}%")
    print(f"{breed_correct_count/IMAGE_AMOUNT*100:.2f}%")
    print(f"{unknown_species_count/IMAGE_AMOUNT*100:.2f}%")
    print(f"{unknown_breed_count/IMAGE_AMOUNT*100:.2f}%")
    print(f"Correct species dict: {species_correct_dict}")
    print(f"Correct breed dict: {breed_correct_dict}\n")

if __name__ == "__main__":
    for i in range(2,10):
        analyze(get_path_from_result_number(i))
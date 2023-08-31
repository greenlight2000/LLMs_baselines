import os
import codecs
import subprocess
import argparse

def save_to_perl_executable(code_str: str, filepath: str = 'output.pl') -> None:
    """Saves given code to a Perl executable."""
    code_str = codecs.decode(code_str, 'unicode_escape')
    with open(filepath, 'w') as f:
        f.write(code_str)
    os.chmod(filepath, 0o755)

def save_codes_from_txt(txt_filepath: str, output_folder: str):
    """Saves lines from a text file as Perl executables in a specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(txt_filepath, 'r') as file:
        lines = file.readlines()
        
        for index, code in enumerate(lines, start=1):
            output_filepath = os.path.join(output_folder, f"{index}.pl")
            save_to_perl_executable(code, output_filepath)
        
    print(f"Saved {len(lines)} Perl files to {output_folder}.")

def execute_perl_script(script_path):
    """Executes a given Perl script and returns its output."""
    try:
        result = subprocess.check_output(['perl', script_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        result = e.output
    return result.replace('\n', ' ').strip()

def execute_all_perl_scripts_in_folder(folder_path, output_txt_path):
    """Executes all Perl scripts in a given folder and saves the outputs to a text file."""
    perl_files = [file for file in os.listdir(folder_path) if file.endswith('.pl')]
    outputs = []

    for perl_file in perl_files:
        file_path = os.path.join(folder_path, perl_file)
        output = execute_perl_script(file_path)
        outputs.append(output)

    with open(output_txt_path, 'w') as file:
        for output in outputs:
            file.write(output + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute Perl scripts and save results.")
    parser.add_argument('--input_txt', default="/path/to/your/source/perl/code.txt", help="Path to the input txt file.")
    parser.add_argument('--output_folder', default="/path/to/save/the/perl/scripts", help="Folder to save the Perl scripts.")
    parser.add_argument('--output_txt', default="/path/to/save/output_results.txt", help="Path to save the output results of perl scripts.")
    args = parser.parse_args()

    save_codes_from_txt(args.input_txt, args.output_folder)
    execute_all_perl_scripts_in_folder(args.output_folder, args.output_txt)
    print(f"Results saved to {args.output_txt}!")

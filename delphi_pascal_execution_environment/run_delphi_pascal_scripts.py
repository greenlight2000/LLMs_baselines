import os
import codecs
import subprocess
import argparse
import re

def save_to_pas_file(code_str: str, filepath: str = 'output.pas') -> None:
    """Saves given code to a PAS file."""
    code_str = codecs.decode(code_str, 'unicode_escape')
    with open(filepath, 'w') as f:
        f.write(code_str)
    os.chmod(filepath, 0o755)

def save_codes_from_txt(txt_filepath: str, output_folder: str):
    """Saves lines from a text file as Delphi programs in a specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(txt_filepath, 'r') as file:
        lines = file.readlines()
        
        for index, code in enumerate(lines, start=1):
            output_filepath = os.path.join(output_folder, f"{index}.pas")
            save_to_pas_file(code, output_filepath)
        
    print(f"Saved {len(lines)} Delphi files to {output_folder}.")

def execute_delphi_script(script_path):
    """Compiles and Executes a given Delphi script and returns its output."""
    base_name = os.path.splitext(os.path.basename(script_path))[0]
    log_name = f"{base_name}_compile.log"
    
    compile_command = f'fpc {script_path} > {log_name}'
    run_command = os.path.join(os.path.dirname(script_path), base_name)
    full_command = f'{compile_command} && {run_command} || cat {log_name}'

    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)

    # Sending an 'Enter' to the process.
    result, _ = process.communicate(input="\n")

    if process.returncode and "timeout" in result:
        return "Script execution timed out after 3 minutes."

    result = re.sub(r".*warning.*\n", "", result)
    return result.replace('\n', ' ').strip()

def execute_all_delphi_scripts_in_folder(folder_path, output_txt_path):
    """Executes all Delphi scripts in a given folder and saves the outputs to a text file."""
    pas_files = [file for file in os.listdir(folder_path) if file.endswith('.pas')]
    outputs = []

    for pas_file in pas_files:
        file_path = os.path.join(folder_path, pas_file)
        output = execute_delphi_script(file_path)
        outputs.append(output)

    with open(output_txt_path, 'w') as file:
        for output in outputs:
            file.write(output + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile and Execute Delphi scripts and save results.")
    parser.add_argument('--input_txt', default="/root/autodl-tmp/delphi.txt", help="Path to the input txt file.")
    parser.add_argument('--output_folder', default="/root/autodl-tmp/delphi/scripts", help="Folder to save the Delphi scripts.")
    parser.add_argument('--output_txt', default="/root/autodl-tmp/delphi/output_results.txt", help="Path to save the output results of Delphi scripts.")
    args = parser.parse_args()

    save_codes_from_txt(args.input_txt, args.output_folder)
    execute_all_delphi_scripts_in_folder(args.output_folder, args.output_txt)
    print(f"Results saved to {args.output_txt}!")

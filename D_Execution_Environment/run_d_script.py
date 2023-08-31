import os
import codecs
import subprocess
import argparse

def save_to_d_executable(code_str: str, filepath: str = 'output.d') -> None:
    """Saves given code to a D executable."""
    code_str = codecs.decode(code_str, 'unicode_escape')
    module_name = "module_name_" + os.path.basename(filepath).replace('.', '_')
    with open(filepath, 'w') as f:
        f.write(f"module {module_name};\n")  # Add module declaration
        f.write(code_str)
    os.chmod(filepath, 0o755)


def save_codes_from_txt(txt_filepath: str, output_folder: str):
    """Saves lines from a text file as D executables in a specified folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(txt_filepath, 'r') as file:
        lines = file.readlines()
        
        for index, code in enumerate(lines, start=1):
            output_filepath = os.path.join(output_folder, f"{index}.d")
            save_to_d_executable(code, output_filepath)
        
    print(f"Saved {len(lines)} D files to {output_folder}.")

def execute_d_script(script_path):
    """Executes a given D script and returns its output."""
    try:
        result = subprocess.check_output(['rdmd', script_path], stderr=subprocess.STDOUT, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return "Script execution timed out after 3 minutes."
    except subprocess.CalledProcessError as e:
        result = e.output
    return result.replace('\n', ' ').strip()


def execute_all_d_scripts_in_folder(folder_path, output_txt_path):
    """Executes all D scripts in a given folder and saves the outputs to a text file."""
    d_files = [file for file in os.listdir(folder_path) if file.endswith('.d')]
    outputs = []

    for d_file in d_files:
        file_path = os.path.join(folder_path, d_file)
        output = execute_d_script(file_path)
        outputs.append(output)

    with open(output_txt_path, 'w') as file:
        for output in outputs:
            file.write(output + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute D scripts and save results.")
    parser.add_argument('--input_txt', default="/root/autodl-tmp/d/d.txt", help="Path to the input txt file.")
    parser.add_argument('--output_folder', default="/root/autodl-tmp/d/scripts", help="Folder to save the D scripts.")
    parser.add_argument('--output_txt', default="/root/autodl-tmp/d/output_results.txt", help="Path to save the output results of D scripts.")
    args = parser.parse_args()

    save_codes_from_txt(args.input_txt, args.output_folder)
    execute_all_d_scripts_in_folder(args.output_folder, args.output_txt)
    print(f"Results saved to {args.output_txt}!")

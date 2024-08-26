# import os.path
import os
import sys



class PathConstants:
    template_path = 'assets/report_template.xlsx'
    output_template_dir = 'reports'
    aym_logo = 'assets/AYM.png'
    kl_logo = 'assets/KL.png'
    if not os.path.exists(output_template_dir):
        os.mkdir(output_template_dir)

    # Get the path of the current script
    script_path = os.path.abspath(sys.argv[0])

    # Get the directory of the script
    project_directory = os.path.dirname(script_path)

import os.path


class PathConstants:
    template_path = 'assets/report_template.xlsx'
    output_template_dir = 'reports'
    aym_logo = 'assets/AYM.png'
    kl_logo = 'assets/KL.png'
    if not os.path.exists(output_template_dir):
        os.mkdir(output_template_dir)

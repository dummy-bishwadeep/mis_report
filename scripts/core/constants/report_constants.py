from openpyxl.styles import Border, Side, Font, Alignment


class ReportConstants:
    # Define border style for cells
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # Define fonts and alignments for various cells
    bold_font = Font(bold=True)
    normal_font = Font(bold=False)
    div_font = Font(size=26, bold=True)  # Font for division headers
    red_font = Font(color="FF0000", bold=True)  # Font for "TOTAL" cells
    rotate_text = Alignment(textRotation=90, horizontal="center", vertical="center")
    center_align = Alignment(horizontal="center", vertical="center")


    sample_data = {
  "lines": [
    {
      "div": "BCF DIV",
      "div_color": "#D9D9F3",
      "energy_color": "#f2f3d9",
      "energy_type": [
        {
          "label": "Power (KWH) Line-1",
          "data": {
            "Machine": 100,
            "Chiller": 200,
            "Air": 300,
            "Uty.Aux.": 400,
            "Lighting & Losses": 500,
            "Dryer": 600,
            "TOTAL": 2100
          }
        },
        {
          "label": "Power (KWH) Line-4A",
          "data": {
            "Machine": 100,
            "Chiller": 200,
            "Air": 300,
            "Uty.Aux.": 400,
            "Lighting & Losses": 500,
            "Dryer": 600,
            "TOTAL": 2100
          }
        }
      ]
    },
    {
      "div": "TEX DIV",
      "div_color": "#d9f3f2",
      "energy_color": "#f3d9d9",
      "energy_type": [
        {
          "label": "Power (KWH) Line-1",
          "data": {
            "Machine": 100,
            "Chiller": 200,
            "Air": 300,
            "Uty.Aux.": 400,
            "Lighting & Losses": 500,
            "Dryer": 600,
            "TOTAL": 2100
          }
        },
        {
          "label": "Power (KWH) Line-4A",
          "data": {
            "Machine": 100,
            "Chiller": 200,
            "Air": 300,
            "Uty.Aux.": 400,
            "Lighting & Losses": 500,
            "Dryer": 600,
            "TOTAL": 2100
          }
        },
        {
          "label": "Power (KWH) Line-4B",
          "data": {
            "Machine": 45,
            "Chiller": 23.1,
            "Air": 21,
            "Uty.Aux.": 67,
            "Lighting & Losses": 11.23,
            "Dryer": 32.8,
            "TOTAL": 121.65
          }
        }
      ]
    }
  ],
  "static_params": {
    "Total Plant Consumption": 100,
    "DNHPDCL Consumption": 200,
    "Solar Power": 300,
    "DG Generation": 400,
    "Total Consumption": 500,
    "HSD Consumption": 600
  },
  "static_color": "#FFFFCC",
  "metadata": {
    "created_by": "AYMAdmin",
    "created_on": "23-08-2024 16:43",
    "report_date": "23-08-2023 15:30"
  }
}
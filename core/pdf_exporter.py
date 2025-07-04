# #PDF
# import pdfkit
# import base64
# import os
# from io import BytesIO
# from datetime import datetime

# import re


# def convert_to_html_list(content):
#     html = ""

#     if isinstance(content, list):
#         html += "<ul>"
#         for item in content:
#             html += f"<li>{item}</li>"
#         html += "</ul>"

#     elif isinstance(content, str):
#         lines = content.strip().split("\n")
#         in_list = False

#         for line in lines:
#             line = line.strip()
#             if re.match(r"^[-*•]\s", line):  # Bullet points
#                 if not in_list:
#                     html += "<ul>"
#                     in_list = True
#                 html += f"<li>{line[2:].strip()}</li>"
#             elif re.match(r"^\d+\.", line):  # Numbered list
#                 if not in_list:
#                     html += "<ol>"
#                     in_list = True
#                 html += f"<li>{line[3:].strip()}</li>"
#             else:
#                 if in_list:
#                     html += "</ul>" if "<ul>" in html else "</ol>"
#                     in_list = False
#                 html += f"<p>{line}</p>"

#         if in_list:
#             html += "</ul>" if "<ul>" in html else "</ol>"

#     return html


# def export_pdf_with_style(score, matched, total, matched_keywords, missing_keywords, summary, skill_gap, suggestions, rewritten):
#     date = datetime.now().strftime("%d %b %Y")
#     html_content = f"""
#     <html>
#     <head>
#         <style>
#             body {{
#                 font-family: "Segoe UI Emoji", "Segoe UI Symbol", "Segoe UI", sans-serif;
#                 font-size: 14px;
#                 padding: 2rem;
#                 color: #333;
#             }}
#             h1 {{
#                 text-align: center;
#                 font-size: 24px;
#                 color: black;
#             }}
#             h2 {{
#                 font-size: 20px;
#                 color: #555;
#                 border-bottom: 1px solid #ccc;
#                 padding-bottom: 4px;
#                 margin-top: 30px;
#             }}
#             .matched {{ color: green; }}
#             .missing {{ color: red; }}
#             ul {{ padding-left: 1.4rem; }}
#             p {{
#                 margin-bottom: 10px;
#             }}
#         </style>

#     </head>
#     <body>

#         <h1>&#10024; JobGenie - Resume Feedback Report &#10024;</h1>
#         <h2>&#128290; Match Score</h2>
#         <p>{score}% ({matched}/{total} keywords matched)</p>

#         <h2 class="matched">&#10004; Matched Skills</h2>
#         <ul>
#             {convert_to_html_list(matched_keywords)}
#         </ul>

#         <h2 class="missing">&#10008; Missing Skills</h2>
#         <ul>
#             {convert_to_html_list(missing_keywords)}
#         </ul>


#         <h2>&#128221; Career Summary</h2>
#         {convert_to_html_list(summary)}

#         <h2>&#128269; Skills Missing</h2>
#         {convert_to_html_list(skill_gap)}

#         <h2>&#127919; Resume Suggestions</h2>
#         {convert_to_html_list(suggestions)}
        
#         <h2>&#128161; Rewritten Resume Bullet</h2>
#         {convert_to_html_list(rewritten)}

#         <p style='margin-top:50px;text-align:center;font-style:italic;color:#888;'>Generated by JobGenie | jobgenie.ai</p>
#     </body>
#     </html>
#     """

#     # Set config for wkhtmltopdf path (update if needed)
#     config = pdfkit.configuration(wkhtmltopdf=r".\wkhtmltopdf\bin\wkhtmltopdf.exe"D:\JobGenie\wkhtmltopdf\bin\wkhtmltopdf.exe)

#     # Generate PDF to memory
#     pdf_bytes = pdfkit.from_string(html_content, False, configuration=config)
#     b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

#     download_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="JobGenie_Styled_Report.pdf"> Download the PDF</a>'
#     return download_link





import streamlit as st
import base64
from datetime import datetime
import re

def convert_to_html_list(content):
    html = ""

    if isinstance(content, list):
        html += "<ul>"
        for item in content:
            html += f"<li>{item}</li>"
        html += "</ul>"

    elif isinstance(content, str):
        lines = content.strip().split("\n")
        in_list = False

        for line in lines:
            line = line.strip()
            if re.match(r"^[-*•]\s", line):  # Bullet points
                if not in_list:
                    html += "<ul>"
                    in_list = True
                html += f"<li>{line[2:].strip()}</li>"
            elif re.match(r"^\d+\.", line):  # Numbered list
                if not in_list:
                    html += "<ol>"
                    in_list = True
                html += f"<li>{line[3:].strip()}</li>"
            else:
                if in_list:
                    html += "</ul>" if "<ul>" in html else "</ol>"
                    in_list = False
                html += f"<p>{line}</p>"

        if in_list:
            html += "</ul>" if "<ul>" in html else "</ol>"

    return html


def generate_html_report(score, matched, total, matched_keywords, missing_keywords, summary, skill_gap, suggestions, rewritten):
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 2rem;
                color: #333;
            }}
            h1 {{
                text-align: center;
                font-size: 24px;
                color: black;
            }}
            h2 {{
                font-size: 20px;
                color: #555;
                border-bottom: 1px solid #ccc;
                padding-bottom: 4px;
                margin-top: 30px;
            }}
            ul {{ padding-left: 1.2rem; }}
            li {{ margin-bottom: 6px; }}
            p {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h1>JobGenie - Resume Feedback Report</h1>
        <h2>Match Score</h2>
        <p>{score}% ({matched}/{total} skills matched)</p>

        <h2>Matched Skills</h2>
        {convert_to_html_list(matched_keywords)}

        <h2>Missing Skills</h2>
        {convert_to_html_list(missing_keywords)}

        <h2>Career Summary</h2>
        {convert_to_html_list(summary)}

        <h2>Skills Gap</h2>
        {convert_to_html_list(skill_gap)}

        <h2>Resume Suggestions</h2>
        {convert_to_html_list(suggestions)}

        <h2>Rewritten Resume Bullet</h2>
        {convert_to_html_list(rewritten)}

        <p style="text-align:center; margin-top:40px; font-size:12px; color:#888;">Generated by JobGenie | jobgenie.ai</p>
    </body>
    </html>
    """
    return html


def download_report_as_html(score, matched, total, matched_keywords, missing_keywords, summary, skill_gap, suggestions, rewritten):
    html = generate_html_report(score, matched, total, matched_keywords, missing_keywords, summary, skill_gap, suggestions, rewritten)
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="JobGenie_Report.html">📥 Download the Report</a>'
    return href

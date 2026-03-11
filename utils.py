import re

# Split advice sections
def split_advice_sections(advice_text):
    advice_text = advice_text.replace("*", "").replace("{", " ").replace("}", " ")
    pattern = r'(Current Financial Health:|Existing Savings Utilization:|Monthly Savings Strategy:|Debt Plan:|Investment Advice:|Goal Guidance:|Budgeting[A-Za-z &]*:)'
    splits = re.split(pattern, advice_text)
    sections = []
    
    for i in range(1, len(splits), 2):
        if i + 1 >= len(splits):
            break
        title = splits[i].strip()
        content = splits[i+1].strip()
        
        if "Current Financial Health" in title:
            content_html = "<p style='margin:0; line-height:1.4em'>" + content.replace("\n", "<br>") + "</p>"
        else:
            content_html = "<ul style='margin:0; padding-left:18px; line-height:1.4em'>"
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("-"):
                    content_html += f"<li>{line[1:].strip()}</li>"
                elif line:
                    content_html += f"<li>{line}</li>"
            content_html += "</ul>"
            
        sections.append((title, content_html))
    return sections

# Split goal sections
def split_goal_sections(goal_text):
    goal_text = goal_text.replace("*", "").replace("{", " ").replace("}", " ")
    pattern = r'(Instruction Implementation Strategy:|Financial Impact Analysis:|Revised Goal Timeline:|Monthly Action Plan:|Resource Allocation Strategy:|Risk Assessment & Mitigation:|Progress Tracking Framework:|Contingency Planning:|Key Success Metrics:|Next Immediate Actions:)'
    splits = re.split(pattern, goal_text)
    sections = []
    
    for i in range(1, len(splits), 2):
        if i + 1 >= len(splits):
            break
        title = splits[i].strip()
        content = splits[i+1].strip()
        
        content_html = "<ul style='margin:0; padding-left:18px; line-height:1.5em'>"
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                content_html += f"<li>{line[1:].strip()}</li>"
            elif line:
                content_html += f"<li>{line}</li>"
        content_html += "</ul>"
        
        sections.append((title, content_html))
    return sections


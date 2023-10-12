import streamlit as st
import pandas as pd
import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from io import BytesIO
import io

st.title("Statement Processing Application Demo")

# Initialize session state keys if not present
if 'uploaded' not in st.session_state:
    st.session_state['uploaded'] = False

if 'data_frame' not in st.session_state:
    st.session_state['data_frame'] = None
    
if 'labels_printed' not in st.session_state:
    st.session_state['labels_printed'] = False


def upload_action():
    st.session_state['uploaded'] = True
    data = {
        'Date': ['2023-10-06', '2023-10-07', '2023-10-08', '2023-10-09', '2023-10-10'],
        'Description': ['Office Supplies Purchase', 'Client Dinner', 'Online Software Subscription', 'Gas Station', 'Grocery Store'],
        'Amount': [-150.00, -200.25, -100.00, -35.00, -75.25],
        'Balance': [122973.12, 122772.87, 122672.87, 122637.87, 122562.62],
    }
    st.session_state['data_frame'] = pd.DataFrame(data)
    st.image("statement.jpg", caption="Pre-configured Statement", use_column_width=True)
    st.table(st.session_state['data_frame'])


def print_labels():
    st.session_state['labels_printed'] = True
    df = st.session_state['data_frame']
    for index, row in df.iterrows():
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(f'{row["Description"]},{row["Amount"]},{row["Balance"]}')
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            doc_buffer = io.BytesIO()
            doc = SimpleDocTemplate(doc_buffer, pagesize=letter)
            elements = []
            qr_image = Image(img_buffer, width=100, height=100)
            data_table = [[f'Description: {row["Description"]}', f'Amount: {row["Amount"]}', f'Balance: {row["Balance"]}'],
                          [qr_image]]
            table = Table(data_table)
            style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 12),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)
            elements.append(table)
            doc.build(elements)

            doc_buffer.seek(0)
            st.download_button(label=f"Download Summary Label {index + 1}", data=doc_buffer,
                               file_name=f'summary_label_{index + 1}.pdf', mime='application/pdf')

st.sidebar.write("""
    Here is a basic proof of concept application that performs some of the fundamental tasks as described in your job post. 
    In this rudimentary hands on example, we are extracting transaction data, and generating summary labels with QR codes which you can download directly.
    The qr codes will coordinate with the data as you'll see once you download the labels.
    
    My hope is that by providing you with a basic example you will consider working with me on your project.
    Having only spent about 2 and half hours or less on this, I am hoping that you will find that if nothing else, I am capable developer that goes above and beyond to deliver in a timely manner.
    
""")

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    if not st.session_state['uploaded'] or st.session_state['labels_printed']:
        st.button("Upload", on_click=upload_action)
    if st.session_state['uploaded'] and not st.session_state['labels_printed']:
        st.button("Print Summary Labels", on_click=print_labels)
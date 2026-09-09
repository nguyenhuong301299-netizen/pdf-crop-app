import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Cắt Nhãn Giao Hàng A6", page_icon="✂️")

st.title("✂️ Cắt Nhãn USPS sang khổ A6")
st.write("Tải file PDF chứa nhãn giao hàng của bạn lên đây. Hệ thống sẽ tự động cắt phần nhãn và chuyển sang kích cỡ chuẩn A6 (dành cho máy in nhiệt).")

# Tải file lên
uploaded_files = st.file_uploader("Chọn file PDF", type="pdf", accept_multiple_files=True)

# Tùy chỉnh vùng cắt (nếu cần)
with st.expander("Tùy chỉnh vùng cắt (Nâng cao)"):
    st.write("Điều chỉnh nếu nhãn của bạn không nằm ở nửa trên cùng của trang giấy:")
    crop_top = st.slider("Cắt từ trên xuống (points)", 0, 400, 20)
    crop_bottom = st.slider("Chiều cao nhãn (points)", 200, 800, 400)
    crop_left = st.slider("Cắt từ trái sang (points)", 0, 200, 20)
    crop_right = st.slider("Chiều rộng nhãn (points)", 200, 600, 580)

if uploaded_files:
    if st.button("Bắt đầu xử lý"):
        for uploaded_file in uploaded_files:
            # Đọc file PDF từ bộ nhớ
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            out_doc = fitz.open()

            # Kích thước A6 (105 x 148 mm) quy đổi ra points
            a6_width = 297.6
            a6_height = 419.5
            a6_rect = fitz.Rect(0, 0, a6_width, a6_height)

            for page in doc:
                # Vùng cắt trên trang gốc (tọa độ lấy theo slider)
                # Dựa vào file mẫu USPS, nhãn thường nằm ở nửa trên
                src_rect = fitz.Rect(crop_left, crop_top, crop_right, crop_top + crop_bottom)
                
                # Tạo trang A6 mới
                new_page = out_doc.new_page(width=a6_width, height=a6_height)
                
                # Chèn phần đã cắt vào trang A6, tự động scale cho vừa
                new_page.show_pdf_page(a6_rect, doc, page.number, clip=src_rect)

            # Xuất ra file mới
            out_bytes = out_doc.write()
            doc.close()
            out_doc.close()

            # Tạo nút tải xuống
            new_file_name = uploaded_file.name.replace(".pdf", "_A6.pdf")
            st.download_button(
                label=f"⬇️ Tải xuống {new_file_name}",
                data=out_bytes,
                file_name=new_file_name,
                mime="application/pdf"
            )
        st.success("Đã xử lý xong! Bạn có thể tải file về.")
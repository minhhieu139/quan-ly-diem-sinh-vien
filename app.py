import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 1. Dữ liệu
data = {
    'Họ tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyên cần': [8.0, 9.0, 7.5, 8.5, 9.0, 6.5, 8.0, 7.0, 7.5, 9.5],
    'Giữa kỳ': [7.0, 8.0, 6.5, 9.0, 7.5, 6.0, 8.5, 7.5, 6.5, 8.5],
    'Cuối kỳ': [8.5, 8.0, 7.0, 8.5, 7.0, 6.5, 9.0, 7.0, 7.5, 9.0]
}

df = pd.DataFrame(data)
df['Tổng kết'] = (0.2 * df['Chuyên cần'] + 0.3 * df['Giữa kỳ'] + 0.5 * df['Cuối kỳ']).round(2)

def xep_loai(diem):
    if diem >= 8.5: return 'Giỏi'
    elif diem >= 7.0: return 'Khá'
    elif diem >= 5.0: return 'Trung bình'
    else: return 'Yếu'

df['Xếp loại'] = df['Tổng kết'].apply(xep_loai)

# 2. Giao diện Streamlit Web App
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

st.subheader("📋 Bảng điểm chi tiết của sinh viên")
st.dataframe(df, use_container_width=True)

# Thống kê
dtb_lop = df['Tổng kết'].mean()
sv_max = df.loc[df['Tổng kết'].idxmax()]
sv_min = df.loc[df['Tổng kết'].idxmin()]
so_dat = (df['Tổng kết'] >= 5.0).sum()

st.subheader("📊 Thống kê chung")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm TB cả lớp", value=f"{dtb_lop:.2f}")
    st.metric(label="Số sinh viên đạt (>= 5)", value=f"{so_dat}/10")
with col2:
    st.metric(label="Cao nhất", value=f"{sv_max['Họ tên']} ({sv_max['Tổng kết']})")
    st.metric(label="Thấp nhất", value=f"{sv_min['Họ tên']} ({sv_min['Tổng kết']})")

# Danh sách xổ xuống chọn sinh viên
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox("Chọn tên sinh viên:", df['Họ tên'].tolist())
student_info = df[df['Họ tên'] == selected_student].iloc[0]

st.info(f"""
* **Họ tên:** {student_info['Họ tên']}
* **Điểm Chuyên cần:** {student_info['Chuyên cần']}
* **Điểm Giữa kỳ:** {student_info['Giữa kỳ']}
* **Điểm Cuối kỳ:** {student_info['Cuối kỳ']}
* **Điểm Tổng kết:** **{student_info['Tổng kết']}**
* **Xếp loại:** **{student_info['Xếp loại']}**
""")

# Biểu đồ cột
st.subheader("📈 Biểu đồ điểm tổng kết của lớp")
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(df['Họ tên'], df['Tổng kết'], color='skyblue')
ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Sinh viên')
ax.set_title('Biểu đồ điểm tổng kết 10 sinh viên')
ax.set_xlim(0, 10)

for index, value in enumerate(df['Tổng kết']):
    ax.text(value + 0.1, index, f"{value}", va='center')

st.pyplot(fig)

# Thông tin người tạo (chữ nhỏ ở cuối trang)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Người tạo: [nguyễn phan minh hiếu] - MSSV: [058208004357]</p>", unsafe_allow_html=True)
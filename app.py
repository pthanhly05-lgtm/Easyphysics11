import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from google import genai

# Cấu hình giao diện
st.set_page_config(
    page_title="Vật Lí 11 (KNTT) - Chương 1: Dao Động",
    page_icon="⚛️",
    layout="wide",
)

# Lấy API Key từ Secrets của Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", "")


def get_ai_client():
  if not api_key:
    st.error("⚠️ Chưa tìm thấy GEMINI_API_KEY trong Streamlit Secrets.")
    return None
  return genai.Client(api_key=api_key)


st.title("⚛️ Ôn Tập Vật Lí 11 - Chương 1: Dao Động (KNTT)")
st.caption(
    "Nền tảng hỗ trợ học tập trực quan & Cá nhân hóa kiến thức với Trợ lý AI"
)

tab1, tab2, tab3 = st.tabs([
    "📊 1. Mô Phỏng & Đồ Thị KNTT",
    "🎯 2. Luyện Tập Trắc Nghiệm AI",
    "🤖 3. Trợ Lý Gia Sư 24/7",
])

# ==============================================================================
# TAB 1: MÔ PHỎNG & ĐỒ THỊ CHUẨN KNTT
# ==============================================================================
with tab1:
  st.subheader("Trực Quan Hóa Khái Niệm & Đồ Thị Vật Lí 11")

  sim_type = st.radio(
      "Chọn mô hình muốn quan sát:",
      [
          "Mối liên hệ giữa Chuyển động tròn đều và Dao động điều hòa",
          "Bộ ba đồ thị Động học (x-t, v-t, a-t) & Đồ thị a-x",
          "Năng lượng (Động năng, Thế năng, Cơ năng) theo t và theo x",
          "Dao động cưỡng bức & Hiện tượng cộng hưởng",
      ],
      horizontal=True,
  )

  # ---------------- 1.1 TRÒN ĐỀU VÀ DAO ĐỘNG ĐIỀU HÒA ----------------
  if (
      sim_type
      == "Mối liên hệ giữa Chuyển động tròn đều và Dao động điều hòa"
  ):
    st.markdown(
        "> **Bản chất (SGK KNTT):** Dao động điều hòa là hình chiếu của một"
        " chất điểm chuyển động tròn đều lên một đường kính quỹ đạo."
    )
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
      A_circ = st.slider("Bán kính R = Biên độ A (cm):", 2.0, 10.0, 5.0, 0.5)
      omega_circ = st.slider("Tốc độ góc ω (rad/s):", 1.0, 6.0, 2.0, 0.5)
      t_snap = st.slider(
          "Thời điểm t (s):",
          0.0,
          float(2 * np.pi / omega_circ),
          0.5,
          0.05,
      )
      alpha = omega_circ * t_snap
      x_snap = A_circ * np.cos(alpha)
      y_snap = A_circ * np.sin(alpha)

      st.info(
          f"Tại thời điểm $t = {t_snap:.2f}\\text{{ s}}$:\n\n"
          f"- Góc quay: $\\alpha = \\omega t = {alpha:.2f}\\text{{ rad}}$\n\n"
          f"- Hình chiếu $x = {x_snap:.2f}\\text{{ cm}}$"
      )
    with col_c2:
      # Vẽ vòng tròn và hình chiếu
      theta = np.linspace(0, 2 * np.pi, 200)
      fig_circle = go.Figure()
      # Quỹ đạo tròn
      fig_circle.add_trace(
          go.Scatter(
              x=A_circ * np.cos(theta),
              y=A_circ * np.sin(theta),
              mode="lines",
              line=dict(color="#bbb", dash="dash"),
              name="Quỹ đạo tròn",
          )
      )
      # Bán kính quay
      fig_circle.add_trace(
          go.Scatter(
              x=[0, x_snap],
              y=[0, y_snap],
              mode="lines+markers",
              line=dict(color="#d62728", width=3),
              name="Bán kính quay OM",
          )
      )
      # Đường dóng hình chiếu
      fig_circle.add_trace(
          go.Scatter(
              x=[x_snap, x_snap],
              y=[y_snap, 0],
              mode="lines",
              line=dict(color="#2ca02c", dash="dot"),
              name="Đường dóng chiếu",
          )
      )
      # Điểm dao động trên trục Ox
      fig_circle.add_trace(
          go.Scatter(
              x=[x_snap],
              y=[0],
              mode="markers",
              marker=dict(size=14, color="#1f77b4"),
              name="Hình chiếu P (Dao động)",
          )
      )
      fig_circle.update_layout(
          xaxis=dict(
              range=[-A_circ * 1.3, A_circ * 1.3],
              zeroline=True,
              zerolinecolor="#333",
              title="Trục Ox (cm)",
          ),
          yaxis=dict(
              range=[-A_circ * 1.3, A_circ * 1.3],
              zeroline=True,
              zerolinecolor="#333",
              scaleanchor="x",
              scaleratio=1,
          ),
          height=420,
          template="plotly_white",
      )
      st.plotly_chart(fig_circle, use_container_width=True)

  # ---------------- 1.2 ĐỒ THỊ ĐỘNG HỌC (x-t, v-t, a-t, a-x) ----------------
  elif sim_type == "Bộ ba đồ thị Động học (x-t, v-t, a-t) & Đồ thị a-x":
    c_p1, c_p2 = st.columns([1, 2])
    with c_p1:
      A = st.slider("Biên độ A (cm):", 1.0, 10.0, 4.0, 0.5)
      omega = st.slider("Tần số góc ω (rad/s):", 1.0, 8.0, 2.0, 0.5)
      phi = st.slider(
          "Pha ban đầu φ (rad):",
          -float(np.pi),
          float(np.pi),
          0.0,
          0.1 * np.pi,
          format="%.2f",
      )
      T = 2 * np.pi / omega
      st.markdown("---")
      st.latex(rf"x = {A}\cos({omega:.1f}t + {phi:.2f})")
      st.latex(
          rf"v = -{A*omega:.1f}\sin({omega:.1f}t + {phi:.2f})"
          rf" = {A*omega:.1f}\cos({omega:.1f}t + {phi:.2f} + \frac{{\pi}}{{2}})"
      )
      st.latex(
          rf"a = -{A*(omega**2):.1f}\cos({omega:.1f}t + {phi:.2f}) = -\omega^2"
          r" x"
      )

    with c_p2:
      t_arr = np.linspace(0, 2 * T, 500)
      x_arr = A * np.cos(omega * t_arr + phi)
      v_arr = -A * omega * np.sin(omega * t_arr + phi)
      a_arr = -A * (omega**2) * np.cos(omega * t_arr + phi)

      sub_fig = make_subplots(
          rows=2,
          cols=1,
          subplot_titles=(
              "Đồ thị biến thiên theo thời gian: x(t), v(t), a(t)",
              "Đồ thị liên hệ a theo x: a = -ω²x (Đoạn thẳng qua gốc O)",
          ),
      )

      # x-t, v-t, a-t chuẩn hóa tỉ lệ vẽ chung
      sub_fig.add_trace(
          go.Scatter(
              x=t_arr,
              y=x_arr,
              name="Li độ x (cm)",
              line=dict(color="#1f77b4", width=2.5),
          ),
          row=1,
          col=1,
      )
      sub_fig.add_trace(
          go.Scatter(
              x=t_arr,
              y=v_arr,
              name="Vận tốc v (cm/s)",
              line=dict(color="#2ca02c", width=1.8, dash="dash"),
          ),
          row=1,
          col=1,
      )
      sub_fig.add_trace(
          go.Scatter(
              x=t_arr,
              y=a_arr,
              name="Gia tốc a (cm/s²)",
              line=dict(color="#d62728", width=1.8, dash="dot"),
          ),
          row=1,
          col=1,
      )

      # a theo x
      x_range = np.linspace(-A, A, 100)
      a_range = -(omega**2) * x_range
      sub_fig.add_trace(
          go.Scatter(
              x=x_range,
              y=a_range,
              name="a theo x",
              line=dict(color="#9467bd", width=3),
          ),
          row=2,
          col=1,
      )

      sub_fig.update_layout(height=520, template="plotly_white")
      sub_fig.update_xaxes(title_text="Thời gian t (s)", row=1, col=1)
      sub_fig.update_xaxes(title_text="Li độ x (cm)", row=2, col=1)
      sub_fig.update_yaxes(title_text="a (cm/s²)", row=2, col=1)
      st.plotly_chart(sub_fig, use_container_width=True)

  # ---------------- 1.3 NĂNG LƯỢNG (THEO t VÀ THEO x) ----------------
  elif (
      sim_type
      == "Năng lượng (Động năng, Thế năng, Cơ năng) theo t và theo x"
  ):
    col_e1, col_e2 = st.columns([1, 2])
    with col_e1:
      m_val = st.slider("Khối lượng vật m (kg):", 0.1, 1.0, 0.2, 0.05)
      A_val = st.slider("Biên độ A (m):", 0.02, 0.1, 0.05, 0.01)
      omega_val = st.slider("Tần số góc ω (rad/s):", 2.0, 10.0, 4.0, 1.0)
      k_val = m_val * (omega_val**2)
      W_val = 0.5 * k_val * (A_val**2)
      st.info(
          f"**Độ cứng tương đương:** $k = m\\omega^2 = {k_val:.1f}\\text{{"           f" N/m}}$\n\n**Cơ năng toàn phần:** $W = \\frac{{1}}{{2}}kA^2 ="
          f" {W_val*1000:.2f}\\text{{ mJ}}$\n\n- Chu kì biến thiên của"
          f" $W_đ, W_t$: $T' = \\frac{{T}}{{2}}$ (tần số góc $2\\omega$)."
      )

    with col_e2:
      plot_mode = st.radio(
          "Xem đồ thị năng lượng theo:",
          ["Theo li độ x (Parabol)", "Theo thời gian t"],
          horizontal=True,
      )

      fig_energy = go.Figure()
      if plot_mode == "Theo li độ x (Parabol)":
        x_pts = np.linspace(-A_val, A_val, 200)
        Wt_x = 0.5 * k_val * (x_pts**2) * 1000  # mJ
        Wd_x = (W_val - 0.5 * k_val * (x_pts**2)) * 1000
        W_line = np.full_like(x_pts, W_val * 1000)

        fig_energy.add_trace(
            go.Scatter(
                x=x_pts,
                y=Wt_x,
                name="Thế năng W_t",
                line=dict(color="#1f77b4", width=2.5),
            )
        )
        fig_energy.add_trace(
            go.Scatter(
                x=x_pts,
                y=Wd_x,
                name="Động năng W_đ",
                line=dict(color="#d62728", width=2.5),
            )
        )
        fig_energy.add_trace(
            go.Scatter(
                x=x_pts,
                y=W_line,
                name="Cơ năng W",
                line=dict(color="#2ca02c", width=2, dash="dash"),
            )
        )
        fig_energy.update_layout(
            title="Đồ thị năng lượng theo li độ x",
            xaxis_title="Li độ x (m)",
            yaxis_title="Năng lượng (mJ)",
            template="plotly_white",
            height=380,
        )
      else:
        t_pts = np.linspace(0, 2 * np.pi / omega_val, 300)
        x_t = A_val * np.cos(omega_val * t_pts)
        v_t = -A_val * omega_val * np.sin(omega_val * t_pts)
        Wt_t = 0.5 * k_val * (x_t**2) * 1000
        Wd_t = 0.5 * m_val * (v_t**2) * 1000
        W_t_line = np.full_like(t_pts, W_val * 1000)

        fig_energy.add_trace(
            go.Scatter(
                x=t_pts,
                y=Wt_t,
                name="Thế năng W_t",
                line=dict(color="#1f77b4", width=2.5),
            )
        )
        fig_energy.add_trace(
            go.Scatter(
                x=t_pts,
                y=Wd_t,
                name="Động năng W_đ",
                line=dict(color="#d62728", width=2.5),
            )
        )
        fig_energy.add_trace(
            go.Scatter(
                x=t_pts,
                y=W_t_line,
                name="Cơ năng W",
                line=dict(color="#2ca02c", width=2, dash="dash"),
            )
        )
        fig_energy.update_layout(
            title="Đồ thị năng lượng theo thời gian t",
            xaxis_title="Thời gian t (s)",
            yaxis_title="Năng lượng (mJ)",
            template="plotly_white",
            height=380,
        )

      st.plotly_chart(fig_energy, use_container_width=True)

  # ---------------- 1.4 DAO ĐỘNG CƯỠNG BỨC & CỘNG HƯỞNG ----------------
  elif sim_type == "Dao động cưỡng bức & Hiện tượng cộng hưởng":
    st.markdown(
        "> **Hiện tượng cộng hưởng (KNTT):** Xảy ra khi tần số của lực cưỡng"
        " bức bằng tần số riêng của hệ dao động ($f = f_0$). Khi đó, biên độ dao"
        " động cưỡng bức đạt giá trị cực đại."
    )
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
      f0 = st.slider("Tần số dao động riêng f₀ (Hz):", 1.0, 5.0, 2.5, 0.5)
      f_cb = st.slider(
          "Tần số ngoại lực cưỡng bức f (Hz):", 0.5, 5.5, 2.0, 0.1
      )
      b_damp = st.slider(
          "Hệ số lực cản môi trường (Ma sát):", 0.2, 1.0, 0.4, 0.1
      )

      diff_f = abs(f_cb - f0)
      if diff_f < 0.15:
        st.success("🚨 ĐANG XẢY RA CỘNG HƯỞNG! Biên độ đạt giá trị cực đại.")
      else:
        st.info("Trạng thái dao động cưỡng bức ổn định.")

    with col_r2:
      # Vẽ đường cong cộng hưởng
      f_domain = np.linspace(0.2, 6.0, 300)
      # Mô hình hàm biên độ Lorentzian xấp xỉ
      A_curve = 1.0 / np.sqrt(((f0**2 - f_domain**2) ** 2) + (b_damp * f_domain) ** 2)
      A_current = 1.0 / np.sqrt(((f0**2 - f_cb**2) ** 2) + (b_damp * f_cb) ** 2)

      fig_res = go.Figure()
      fig_res.add_trace(
          go.Scatter(
              x=f_domain,
              y=A_curve,
              mode="lines",
              line=dict(color="#1f77b4", width=2.5),
              name="Đường cong cộng hưởng",
          )
      )
      fig_res.add_trace(
          go.Scatter(
              x=[f_cb],
              y=[A_current],
              mode="markers",
              marker=dict(size=14, color="#d62728"),
              name="Điểm làm việc hiện tại",
          )
      )
      fig_res.add_vline(
          x=f0,
          line_dash="dot",
          line_color="#2ca02c",
          annotation_text=f"f₀ = {f0} Hz",
      )
      fig_res.update_layout(
          title="Đồ thị biên độ dao động cưỡng bức theo tần số ngoại lực",
          xaxis_title="Tần số ngoại lực f (Hz)",
          yaxis_title="Biên độ dao động cưỡng bức A",
          template="plotly_white",
          height=380,
      )
      st.plotly_chart(fig_res, use_container_width=True)

# ==============================================================================
# TAB 2: LUYỆN TẬP TRẮC NGHIỆM AI THEO MA TRẬN KNTT
# ==============================================================================
with tab2:
  st.header("Luyện Tập Trắc Nghiệm Thông Minh (Chuẩn KNTT)")
  col_s1, col_s2 = st.columns(2)

  with col_s1:
    topic_kntt = st.selectbox(
        "Chuyên đề ôn tập (SGK KNTT):",
        [
            "1. Dao động điều hòa và Chuyển động tròn đều (Li độ, chu kì, tần số, pha ban đầu)",
            "2. Mối liên hệ pha & Đồ thị li độ, vận tốc, gia tốc (x-t, v-t, a-t, a-x)",
            "3. Con lắc lò xo và Con lắc đơn (Chu kì, tần số, điều kiện dao động điều hòa)",
            "4. Động năng, Thế năng & Sự bảo toàn cơ năng trong dao động điều hòa",
            "5. Đồ thị chuyển hóa năng lượng theo li độ x và theo thời gian t",
            "6. Dao động tắt dần, Dao động cưỡng bức và Hiện tượng cộng hưởng",
        ],
    )
  with col_s2:
    level_kntt = st.selectbox(
        "Mức độ câu hỏi:",
        [
            "Nhận biết (Định nghĩa, công thức cơ bản)",
            "Thông hiểu (Đọc đồ thị, so sánh pha, tính toán 1 bước)",
            "Vận dụng (Bài toán tổng hợp năng lượng, thời gian, liên hệ thực tế)",
        ],
    )

  if st.button("✨ Sinh bộ câu hỏi trắc nghiệm mới"):
    client = get_ai_client()
    if client:
      with st.spinner("AI đang biên soạn đề trắc nghiệm..."):
        prompt_quiz = f"""
                Bạn là chuyên gia giảng dạy Vật lí 11 theo bộ sách Kết nối tri thức với cuộc sống (KNTT).
                Hãy tạo đúng 3 câu hỏi trắc nghiệm 4 lựa chọn (A, B, C, D) về chuyên đề: "{topic_kntt}", mức độ: "{level_kntt}".
                Quy định bắt buộc:
                1. Mọi biểu thức toán/vật lí, biến số phải được đặt trong cặp dấu $...$ chuẩn LaTeX (ví dụ: $x = 4\\cos(2\\pi t + \\frac{{\\pi}}{{3}})$, $\\text{{rad/s}}$, $W_đ$, $W_t$).
                2. Nếu câu hỏi liên quan đến đồ thị hoặc bảng số liệu, hãy mô tả rõ ràng các mốc tọa độ trong đề bài.
                3. Trả về đúng định dạng JSON thuần túy (không dùng block code ```json, không thêm chữ thừa):
                [
                  {{
                    "question": "Nội dung câu hỏi...",
                    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
                    "correct_answer": "A. ...",
                    "explanation": "Lời giải chi tiết từng bước, viện dẫn công thức SGK KNTT..."
                  }}
                ]
                """
        try:
          resp = client.models.generate_content(
              model="gemini-2.5-flash", contents=prompt_quiz
          )
          cleaned_text = resp.text.strip()
          if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:-3].strip()
          elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:-3].strip()
          st.session_state["kntt_quiz"] = json.loads(cleaned_text)
        except Exception as err:
          st.error(f"Lỗi khi sinh câu hỏi: {err}")

  if "kntt_quiz" in st.session_state and st.session_state["kntt_quiz"]:
    quiz_data = st.session_state["kntt_quiz"]
    with st.form("kntt_form"):
      ans = {}
      for idx, item in enumerate(quiz_data):
        st.markdown(f"**Câu {idx+1}:** {item['question']}")
        ans[idx] = st.radio(
            "Chọn đáp án:",
            item["options"],
            key=f"kntt_ans_{idx}",
            label_visibility="collapsed",
        )
        st.write("---")
      submitted = st.form_submit_button("Nộp bài & Xem phân tích chi tiết")

    if submitted:
      score = 0
      for idx, item in enumerate(quiz_data):
        if ans[idx] == item["correct_answer"]:
          score += 1
          st.success(f"Câu {idx+1}: Chính xác! 🎉")
        else:
          st.error(
              f"Câu {idx+1}: Chưa đúng. Đáp án chuẩn là:"
              f" {item['correct_answer']}"
          )
        st.info(f"💡 **Hướng dẫn giải chi tiết:**\n{item['explanation']}")
      st.metric(
          label="Tổng kết kết quả",
          value=f"{score}/{len(quiz_data)} điểm",
          delta=f"{int(score/len(quiz_data)*10)}/10",
      )

# ==============================================================================
# TAB 3: TRỢ LÝ GIA SƯ AI (CHUYÊN TRÁCH VẬT LÍ 11 KNTT)
# ==============================================================================
with tab3:
  st.header("Gia Sư Trực Tuyến 24/7 (Sách Kết Nối Tri Thức)")
  st.caption(
      "Giải đáp cặn kẽ mọi thắc mắc về hiện tượng, phương pháp đọc đồ thị,"
      " chứng minh công thức Chương 1."
  )

  if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [{
        "role": "assistant",
        "content": (
            "Chào em! Thầy/cô là Trợ lý AI môn Vật lí 11 bộ Kết nối tri thức."
            " Em đang gặp vướng mắc ở khái niệm, đồ thị hay bài tập nào của"
            " Chương 1?"
        ),
    }]

  for chat in st.session_state["chat_history"]:
    with st.chat_message(chat["role"]):
      st.markdown(chat["content"])

  user_question = st.chat_input("Nhập câu hỏi của em...")

  if user_question:
    st.session_state["chat_history"].append(
        {"role": "user", "content": user_question}
    )
    with st.chat_message("user"):
      st.markdown(user_question)

    client = get_ai_client()
    if client:
      with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu kiến thức KNTT và phản hồi..."):
          system_ctx = """
                    Bạn là Trợ lý Giáo viên Vật lí THPT, am hiểu tường tận chương trình GDPT 2018 và SGK Vật lí 11 bộ Kết nối tri thức với cuộc sống (Chương 1: Dao động).
                    Nguyên tắc trả lời:
                    1. Bám sát thuật ngữ và định nghĩa của SGK KNTT (dao động tự do, dao động điều hòa, pha dao động, sự lệch pha giữa x, v, a; biến thiên năng lượng; hiện tượng cộng hưởng).
                    2. Giải thích ngắn gọn, sư phạm, có ví dụ hoặc liên hệ thực tế, kích thích học sinh tự suy luận.
                    3. Nhắc học sinh phân biệt rõ "giá trị" (có âm có dương) và "độ lớn/tốc độ" (luôn không âm): v_max = ωA, v_min = -ωA; Tốc độ cực tiểu: |v|_min = 0 (tại biên). a_max = ω²A (biên âm), a_min = -ω²A (biên dương); Độ lớn gia tốc cực tiểu: |a|_min = 0 (ở VTCB).
                    4. Công thức năng lượng con lắc lò xo và con lắc đơn góc nhỏ (dùng cả α và s).
                    5. Tất cả công thức và biến số phải định dạng LaTeX chuẩn ($...$).
                    """
          prompt_to_bot = (
              f"{system_ctx}\n\nHọc sinh hỏi: {user_question}\nGiáo viên trả"
              " lời:"
          )
          try:
            res_bot = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt_to_bot
            ).text
            st.markdown(res_bot)
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": res_bot}
            )
          except Exception as ex:
            st.error(f"Lỗi: {ex}")

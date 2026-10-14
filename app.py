import os
import io
import tempfile
import base64
import streamlit as st
import streamlit.components.v1 as components
from pdf2docx import Converter

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Multi-Format Converter",
    page_icon="🔄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Brand Color Tokens & SaaS Modern Styles
# Primary Blue: #429ec2 | Primary Green: #83bd64
# Dark Background: #0a0e17 | Card: #121a2b
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Google Fonts: Inter & Material Symbols */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    /* Global Reset & Base Typography */
    html, body, .stApp, p, h1, h2, h3, h4, h5, h6, label, input {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #f1f5f9;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Subtle Modern SaaS Cursor Follower Glow */
    #app-cursor-glow {
        position: fixed;
        top: 0;
        left: 0;
        width: 480px;
        height: 480px;
        border-radius: 50%;
        pointer-events: none !important;
        z-index: 0;
        transform: translate3d(-1000px, -1000px, 0);
        background: radial-gradient(
            circle,
            rgba(66, 158, 194, 0.14) 0%,
            rgba(131, 189, 100, 0.07) 38%,
            transparent 68%
        );
        filter: blur(40px);
        opacity: 0;
        transition: opacity 0.45s ease;
        will-change: transform, opacity;
    }

    /* Zero-height iframe handling */
    iframe[height="0"],
    [data-testid="stCustomComponentV1"]:has(iframe[height="0"]) {
        position: fixed !important;
        top: -9999px !important;
        left: -9999px !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Preserve Material Symbols and Icon fonts */
    span[translate="no"],
    [data-testid*="Icon"],
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    [class*="material-symbols"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* Dark App Background with Subtle Glow Mesh */
    .stApp {
        background-color: #0a0e17 !important;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(66, 158, 194, 0.12) 0%, rgba(131, 189, 100, 0.06) 35%, transparent 68%),
            radial-gradient(circle at 85% 90%, rgba(66, 158, 194, 0.04) 0%, transparent 40%) !important;
        background-attachment: fixed !important;
    }

    /* Completely hide empty style containers */
    [data-testid="stElementContainer"]:has(style),
    .element-container:has(style) {
        display: none !important;
        position: absolute !important;
        height: 0 !important;
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    /* Hide Streamlit default header, toolbar, running status, and decoration completely */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    header,
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stToolbar"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        visibility: hidden !important;
    }
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}

    /* Centered Compact SaaS Card Layout */
    .block-container {
        max-width: 680px !important;
        padding: 1.8rem 2rem 2rem 2rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 2rem !important;
        background: #121a2b !important;
        border: 1px solid rgba(66, 158, 194, 0.22) !important;
        border-radius: 18px !important;
        box-shadow: 
            0 24px 48px -12px rgba(0, 0, 0, 0.6),
            0 0 0 1px rgba(255, 255, 255, 0.04),
            0 0 32px -8px rgba(66, 158, 194, 0.12) !important;
        position: relative !important;
        transition: box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s ease, transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .block-container:hover {
        border-color: rgba(66, 158, 194, 0.38) !important;
        box-shadow: 
            0 28px 56px -12px rgba(0, 0, 0, 0.7),
            0 0 0 1px rgba(255, 255, 255, 0.06),
            0 0 44px -6px rgba(66, 158, 194, 0.22) !important;
        transform: translateY(-1px) !important;
    }

    /* Top Gradient Accent Line */
    .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #429ec2 0%, #83bd64 100%);
        border-top-left-radius: 18px;
        border-top-right-radius: 18px;
    }

    /* App Header */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.85rem;
        margin-top: 0 !important;
        margin-bottom: 0.3rem;
    }

    .app-header-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(66, 158, 194, 0.16) 0%, rgba(131, 189, 100, 0.16) 100%);
        border: 1px solid rgba(66, 158, 194, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        flex-shrink: 0;
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s ease;
    }

    .app-header:hover .app-header-icon {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 20px rgba(66, 158, 194, 0.35);
    }

    .app-header-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f8fafc 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.03em;
        margin: 0;
        line-height: 1.2;
    }

    .app-header-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        margin: 0.2rem 0 1rem 0;
        line-height: 1.4;
        text-align: center;
    }

    /* Modern SaaS Trust Badges */
    .trust-badge-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        padding: 0;
        background: transparent;
        border: none;
        margin-bottom: 2rem;
        width: 100%;
    }

    .trust-item {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.72rem;
        font-weight: 600;
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        letter-spacing: 0.02em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
    }
    
    .trust-item:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(66, 158, 194, 0.3);
        transform: translateY(-1px);
    }

    .trust-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        display: inline-block;
    }

    .trust-dot.blue {
        background-color: #429ec2;
        box-shadow: 0 0 6px rgba(66, 158, 194, 0.7);
    }

    .trust-dot.green {
        background-color: #83bd64;
        box-shadow: 0 0 6px rgba(131, 189, 100, 0.7);
    }
    
    .trust-divider { display: none; }

    /* Section Labels */
    .section-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #71849d;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }

    /* Cards - Clean Modern Responsive Grid */
    div[data-testid="stRadio"] {
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        margin-bottom: 1.5rem;
    }

    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 12px !important;
        width: 100% !important;
    }

    div[data-testid="stRadio"] label {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        background: rgba(18, 26, 43, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 14px !important;
        padding: 1rem 0.5rem !important;
        margin: 0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
        transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        width: calc(33.333% - 8px) !important;
        min-width: 130px !important;
        min-height: 80px !important;
    }

    div[data-testid="stRadio"] label:hover {
        color: #f1f5f9 !important;
        background: rgba(30, 41, 59, 0.9) !important;
        border-color: rgba(66, 158, 194, 0.3) !important;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3), 0 0 15px rgba(66, 158, 194, 0.1) !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked) {
        background: rgba(18, 26, 43, 0.9) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: 1.5px solid #429ec2 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), 0 0 20px rgba(66, 158, 194, 0.25) !important;
        transform: translateY(-2px);
    }
    
    div[data-testid="stRadio"] label[data-checked="true"]::after,
    div[data-testid="stRadio"] label:has(input:checked)::after {
        display: none !important;
    }

    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] {
        width: 100%;
        text-align: center;
    }

    /* -----------------------------------------------------
       Native Streamlit File Uploader Clean SaaS Styling
       ----------------------------------------------------- */
    [data-testid="stFileUploader"] {
        margin-bottom: 1.1rem;
    }

    /* Hide any duplicate widget labels */
    [data-testid="stFileUploader"] > label,
    [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] {
        display: none !important;
    }

    /* Clean, centered, clickable dropzone */
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploader"] section {
        border: 1.5px dashed rgba(66, 158, 194, 0.35) !important;
        border-radius: 14px !important;
        background-color: #0b111e !important;
        padding: 2rem 1.4rem !important;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: center !important;
        cursor: pointer !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.45rem !important;
        min-height: 180px !important;
        position: relative !important;
    }

    [data-testid="stFileUploaderDropzone"]:hover,
    [data-testid="stFileUploader"] section:hover {
        border-color: #429ec2 !important;
        background-color: rgba(66, 158, 194, 0.05) !important;
        box-shadow: 0 0 24px rgba(66, 158, 194, 0.18), inset 0 0 16px rgba(131, 189, 100, 0.04) !important;
        transform: translateY(-2px) !important;
    }

    /* Clean SVG Upload Icon at top of dropzone */
    [data-testid="stFileUploaderDropzone"]::before,
    [data-testid="stFileUploader"] section::before {
        content: '';
        display: block;
        width: 40px;
        height: 40px;
        margin-bottom: 0.2rem;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23429ec2' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3Cpolyline points='17 8 12 3 7 8'/%3E%3Cline x1='12' y1='3' x2='12' y2='15'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        transition: transform 0.25s ease, filter 0.25s ease;
    }

    [data-testid="stFileUploaderDropzone"]:hover::before,
    [data-testid="stFileUploader"] section:hover::before {
        transform: scale(1.1) translateY(-2px);
        filter: drop-shadow(0 0 8px rgba(66, 158, 194, 0.6));
    }

    /* Dropzone instructions - "Drop your file here" + "or browse from your computer" */
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        text-align: center !important;
        margin-top: 0.1rem !important;
        order: 2 !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "Drop your file here";
        display: block;
        font-size: 0.98rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.15rem;
        letter-spacing: -0.01em;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] small,
    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #71849d !important;
        font-size: 0.78rem !important;
        display: block !important;
        font-weight: 400 !important;
    }

    /* Single clean Browse files button */
    [data-testid="stFileUploader"] button {
        border-radius: 8px !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        border: 1px solid rgba(66, 158, 194, 0.35) !important;
        background: rgba(66, 158, 194, 0.12) !important;
        color: #429ec2 !important;
        padding: 0.45rem 1.25rem !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        margin-top: 0.45rem !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        order: 3 !important;
    }

    /* Hide inner button elements to eliminate duplicate upload/Upload text */
    [data-testid="stFileUploader"] button span[translate="no"],
    [data-testid="stFileUploader"] button [data-testid="stIconMaterial"],
    [data-testid="stFileUploader"] button p,
    [data-testid="stFileUploader"] button div[data-testid="stMarkdownContainer"] {
        display: none !important;
    }

    /* Single clean "Browse Files" text inside button */
    [data-testid="stFileUploader"] button::after {
        content: "Browse Files";
        display: inline-block;
        font-size: 0.84rem;
        font-weight: 600;
        color: inherit;
    }

    [data-testid="stFileUploader"] button:hover {
        border-color: #429ec2 !important;
        background: #429ec2 !important;
        color: #ffffff !important;
        box-shadow: 0 0 16px rgba(66, 158, 194, 0.45) !important;
        transform: translateY(-1px) scale(1.02) !important;
    }

    /* Hide Streamlit default file list row to use custom preview card */
    [data-testid="stFileUploaderFile"] {
        display: none !important;
    }

    /* Uploaded File Preview Card */
    .file-preview-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0b111e;
        border: 1px solid rgba(66, 158, 194, 0.35);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-top: 0.2rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
        transition: all 0.25s ease;
    }

    .file-preview-card:hover {
        border-color: rgba(66, 158, 194, 0.55);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), 0 0 14px rgba(66, 158, 194, 0.15);
        transform: translateY(-1px);
    }

    .file-preview-left {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        overflow: hidden;
        flex: 1;
    }

    .file-preview-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 10px;
        background: rgba(66, 158, 194, 0.15);
        color: #429ec2;
        font-size: 1.25rem;
        flex-shrink: 0;
        border: 1px solid rgba(66, 158, 194, 0.25);
    }

    .file-preview-icon.green {
        background: rgba(131, 189, 100, 0.15);
        color: #83bd64;
        border-color: rgba(131, 189, 100, 0.25);
    }

    .file-thumbnail-img {
        width: 44px;
        height: 44px;
        border-radius: 9px;
        object-fit: cover;
        flex-shrink: 0;
        border: 1px solid rgba(66, 158, 194, 0.3);
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .file-preview-details {
        display: flex;
        flex-direction: column;
        overflow: hidden;
        flex: 1;
    }

    .file-preview-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #f1f5f9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 280px;
    }

    .file-preview-meta {
        font-size: 0.76rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-top: 0.15rem;
        flex-wrap: wrap;
    }

    .file-preview-meta-pill {
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 500;
    }

    .file-preview-badge {
        font-size: 0.72rem;
        color: #83bd64;
        background: rgba(131, 189, 100, 0.12);
        border: 1px solid rgba(131, 189, 100, 0.28);
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 600;
        flex-shrink: 0;
        margin-left: 0.5rem;
    }

    /* Visual preview expansion box */
    .file-visual-preview-box {
        background: #090e18;
        border: 1px solid rgba(66, 158, 194, 0.25);
        border-radius: 12px;
        padding: 0.85rem;
        margin-bottom: 1.1rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .file-visual-preview-box img {
        max-height: 180px;
        max-width: 100%;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.08);
        object-fit: contain;
    }

    .file-visual-preview-caption {
        font-size: 0.74rem;
        color: #71849d;
        text-align: center;
    }

    /* Empty state info card */
    .upload-empty-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.45rem;
        flex-wrap: wrap;
        margin-top: -0.4rem;
        margin-bottom: 1.1rem;
        font-size: 0.75rem;
        color: #71849d;
    }

    .upload-empty-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.07);
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        font-weight: 500;
        color: #94a3b8;
    }

    /* Professional SaaS Progress Box */
    .progress-box {
        background: #0b111e;
        border: 1px solid rgba(66, 158, 194, 0.35);
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        margin: 1rem 0;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35), 0 0 16px rgba(66, 158, 194, 0.1);
    }

    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.65rem;
    }

    .progress-title-left {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.88rem;
        font-weight: 600;
        color: #f1f5f9;
    }

    .progress-percent {
        font-size: 0.84rem;
        font-weight: 700;
        color: #429ec2;
        font-variant-numeric: tabular-nums;
    }

    .progress-track {
        height: 7px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        overflow: hidden;
        position: relative;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #429ec2 0%, #83bd64 100%);
        border-radius: 999px;
        transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 10px rgba(66, 158, 194, 0.5);
    }

    .progress-step-text {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Recent Conversions Section */
    .recent-section {
        margin-top: 1.8rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(66, 158, 194, 0.18);
    }

    .recent-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #090e18;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 0.6rem 0.85rem;
        margin-bottom: 0.45rem;
        font-size: 0.8rem;
        transition: all 0.2s ease;
    }

    .recent-item:hover {
        border-color: rgba(66, 158, 194, 0.3);
        background: #0e1524;
        transform: translateY(-1px);
    }

    .recent-item-left {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        overflow: hidden;
    }

    .recent-type-badge {
        font-size: 0.7rem;
        font-weight: 600;
        color: #429ec2;
        background: rgba(66, 158, 194, 0.12);
        border: 1px solid rgba(66, 158, 194, 0.25);
        padding: 2px 7px;
        border-radius: 5px;
        white-space: nowrap;
        flex-shrink: 0;
    }

    .recent-filenames {
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .recent-orig-name {
        color: #cbd5e1;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 220px;
        font-size: 0.8rem;
    }

    .recent-out-name {
        color: #83bd64;
        font-size: 0.72rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 220px;
    }

    .recent-time {
        font-size: 0.7rem;
        color: #64748b;
        flex-shrink: 0;
        margin-left: 0.5rem;
    }

    /* Small Remove Button Icon Styling */
    div[data-testid="stButton"] button[key^="remove_file_"] {
        padding: 0.3rem 0.6rem !important;
        min-height: 32px !important;
        font-size: 0.78rem !important;
        color: #fca5a5 !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        background: rgba(239, 68, 68, 0.08) !important;
    }

    div[data-testid="stButton"] button[key^="remove_file_"]:hover {
        background: rgba(239, 68, 68, 0.18) !important;
        border-color: #ef4444 !important;
        color: #ffffff !important;
    }

    /* Responsive Design Adjustments */
    @media (max-width: 640px) {
        .block-container {
            padding: 1.2rem 1.1rem 1.4rem 1.1rem !important;
            margin-top: 0.5rem !important;
            border-radius: 14px !important;
        }

        .app-header-title {
            font-size: 1.35rem !important;
        }

        div[data-testid="stRadio"] label {
            width: calc(50% - 6px) !important;
            min-width: 110px !important;
            min-height: 70px !important;
            padding: 0.75rem 0.4rem !important;
        }

        .file-preview-name {
            max-width: 170px !important;
        }

        .recent-orig-name, .recent-out-name {
            max-width: 140px !important;
        }
    }

    /* Primary Action Button (Convert Document) */
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"],
    div.stButton > button[data-testid="stBaseButton-primary"],
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"],
    div.stButton > button:not(:disabled):not([kind="secondary"]):not([data-testid*="secondary"]) {
        background: linear-gradient(135deg, #429ec2 0%, #3585a6 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1.2rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        box-shadow: 0 4px 16px rgba(66, 158, 194, 0.32) !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 44px !important;
    }

    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="baseButton-primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover,
    div[data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover,
    div.stButton > button:not(:disabled):not([kind="secondary"]):not([data-testid*="secondary"]):hover {
        background: linear-gradient(135deg, #4daed4 0%, #3a91b5 100%) !important;
        box-shadow: 0 6px 22px rgba(66, 158, 194, 0.48), 0 0 12px rgba(131, 189, 100, 0.2) !important;
        transform: translateY(-2px);
    }

    div.stButton > button:active,
    div[data-testid="stButton"] button:active {
        transform: translateY(0px) !important;
    }

    /* Disabled Action Button */
    div.stButton > button:disabled,
    div.stButton > button[disabled],
    div[data-testid="stButton"] button:disabled,
    div[data-testid="stButton"] button[disabled] {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #64748b !important;
        box-shadow: none !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        cursor: not-allowed !important;
        transform: none !important;
        min-height: 44px !important;
    }

    /* Secondary Clear Button */
    div.stButton > button[kind="secondary"]:not(:disabled),
    div.stButton > button[data-testid="baseButton-secondary"]:not(:disabled),
    div.stButton > button[data-testid="stBaseButton-secondary"]:not(:disabled),
    div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:not(:disabled) {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #94a3b8 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.65rem 1rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: none !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-height: 44px !important;
    }

    div.stButton > button[kind="secondary"]:not(:disabled):hover,
    div.stButton > button[data-testid="baseButton-secondary"]:not(:disabled):hover,
    div.stButton > button[data-testid="stBaseButton-secondary"]:not(:disabled):hover,
    div[data-testid="stButton"] button[data-testid="stBaseButton-secondary"]:not(:disabled):hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #f1f5f9 !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-1px);
    }

    div.stButton > button p,
    div[data-testid="stButton"] button p {
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }

    /* Success Result Card */
    .success-card {
        background: rgba(131, 189, 100, 0.07);
        border: 1px solid rgba(131, 189, 100, 0.3);
        border-left: 4px solid #83bd64;
        border-radius: 12px;
        padding: 1.05rem 1.2rem;
        margin-top: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.4), 0 0 16px rgba(131, 189, 100, 0.1);
        transition: all 0.25s ease;
    }

    .success-card:hover {
        box-shadow: 0 10px 28px -6px rgba(0, 0, 0, 0.5), 0 0 20px rgba(131, 189, 100, 0.18);
        transform: translateY(-1px);
    }

    .success-header {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.25rem;
    }

    .success-icon-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: #83bd64;
        color: #0b111e;
        font-size: 0.78rem;
        font-weight: 800;
        flex-shrink: 0;
    }

    .success-title {
        font-size: 0.94rem;
        font-weight: 700;
        color: #f1f5f9;
        letter-spacing: -0.01em;
    }

    .success-desc {
        font-size: 0.82rem;
        color: #94a3b8;
        margin: 0 0 0.6rem 1.95rem;
    }

    .success-meta {
        font-size: 0.8rem;
        color: #cbd5e1;
        background: rgba(131, 189, 100, 0.1);
        border: 1px solid rgba(131, 189, 100, 0.2);
        border-radius: 8px;
        padding: 0.4rem 0.75rem;
        margin-left: 1.95rem;
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
    }

    .success-meta b {
        color: #ffffff;
    }

    /* Download Button (Brand Green CTA) */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #83bd64 0%, #6da650 100%) !important;
        color: #ffffff !important;
        font-size: 0.93rem !important;
        font-weight: 700 !important;
        padding: 0.7rem 1.25rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 4px 18px rgba(131, 189, 100, 0.35) !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        min-height: 46px !important;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #91cc72 0%, #76b457 100%) !important;
        box-shadow: 0 6px 24px rgba(131, 189, 100, 0.5), 0 0 14px rgba(66, 158, 194, 0.2) !important;
        transform: translateY(-2px);
    }

    /* Professional Error Alert Card */
    .error-card {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 0.95rem 1.15rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }

    .error-card-title {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.88rem;
        font-weight: 600;
        color: #fca5a5;
        margin-bottom: 0.25rem;
    }

    .error-card-desc {
        font-size: 0.82rem;
        color: #e2e8f0;
        line-height: 1.45;
        padding-left: 1.45rem;
    }

    /* Streamlit Spinner Accent */
    div[data-testid="stSpinner"] {
        color: #429ec2 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Subtle Smooth SaaS Cursor Glow Animation
# ---------------------------------------------------------
components.html("""
<script>
(function() {
    try {
        const pDoc = window.parent.document;
        const pWin = window.parent;
        if (!pDoc) return;
        
        let glow = pDoc.getElementById('app-cursor-glow');
        if (!glow) {
            glow = pDoc.createElement('div');
            glow.id = 'app-cursor-glow';
            pDoc.body.appendChild(glow);
        }

        let mouseX = -1000, mouseY = -1000;
        let currentX = -1000, currentY = -1000;
        let isVisible = false;

        const onMouseMove = (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            if (!isVisible) {
                isVisible = true;
                glow.style.opacity = '1';
                currentX = mouseX;
                currentY = mouseY;
            }
        };

        const onMouseLeave = () => {
            isVisible = false;
            glow.style.opacity = '0';
        };

        if (pWin._pdfAppMouseMove) {
            pDoc.removeEventListener('mousemove', pWin._pdfAppMouseMove);
        }
        if (pWin._pdfAppMouseLeave) {
            pDoc.removeEventListener('mouseleave', pWin._pdfAppMouseLeave);
        }

        pWin._pdfAppMouseMove = onMouseMove;
        pWin._pdfAppMouseLeave = onMouseLeave;

        pDoc.addEventListener('mousemove', onMouseMove, { passive: true });
        pDoc.addEventListener('mouseleave', onMouseLeave, { passive: true });

        function renderLoop() {
            if (isVisible) {
                currentX += (mouseX - currentX) * 0.12;
                currentY += (mouseY - currentY) * 0.12;
                glow.style.transform = `translate3d(${Math.round(currentX - 240)}px, ${Math.round(currentY - 240)}px, 0)`;
            }
            pWin.requestAnimationFrame(renderLoop);
        }

        if (!pWin._pdfAppGlowLoopRunning) {
            pWin._pdfAppGlowLoopRunning = true;
            pWin.requestAnimationFrame(renderLoop);
        }
    } catch(err) {
        // Safe fallback
    }
})();
</script>
""", height=0, width=0)

# ---------------------------------------------------------
# Constants & Helpers
# ---------------------------------------------------------
PDF_TO_WORD  = "📄 PDF → Word"
WORD_TO_PDF  = "📝 Word → PDF"
IMG_TO_PDF   = "🖼️ Image → PDF"
PDF_TO_IMG   = "🔍 PDF → Image"
PDF_TO_EXCEL = "📊 PDF → Excel"
PDF_TO_PPTX  = "📽️ PDF → PowerPoint"
PDF_TO_TXT   = "📃 PDF → TXT"

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


def format_size(size_bytes: int) -> str:
    """Formats bytes into human readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1048576:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1048576:.2f} MB"


def get_file_metadata(file_bytes: bytes, filename: str) -> dict:
    """Extracts informative SaaS file metadata like format, page count, or dimensions."""
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    meta = {
        "ext": ext.upper() if ext else "FILE",
        "size_str": format_size(len(file_bytes)),
        "page_count": None,
        "dimensions": None,
        "type_label": ext.upper() if ext else "File"
    }

    if ext == "pdf":
        meta["type_label"] = "PDF Document"
        try:
            import pymupdf
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            meta["page_count"] = len(doc)
            doc.close()
        except Exception:
            pass
    elif ext in ("jpg", "jpeg", "png"):
        meta["type_label"] = f"Image ({ext.upper()})"
        try:
            from PIL import Image
            with Image.open(io.BytesIO(file_bytes)) as img:
                meta["dimensions"] = f"{img.width}×{img.height}"
        except Exception:
            pass
    elif ext == "docx":
        meta["type_label"] = "Word Document"
    elif ext == "txt":
        meta["type_label"] = "Plain Text"

    return meta


def generate_thumbnail(file_bytes: bytes, filename: str) -> str:
    """Generates a small base64 data URI preview thumbnail for PDFs and images."""
    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    try:
        if ext == "pdf":
            import pymupdf
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            if len(doc) > 0:
                page = doc[0]
                # Small thumbnail scale
                pix = page.get_pixmap(matrix=pymupdf.Matrix(0.5, 0.5), alpha=False)
                png_bytes = pix.tobytes("png")
                doc.close()
                b64 = base64.b64encode(png_bytes).decode("ascii")
                return f"data:image/png;base64,{b64}"
            doc.close()
        elif ext in ("jpg", "jpeg", "png"):
            from PIL import Image
            with Image.open(io.BytesIO(file_bytes)) as img:
                img_copy = img.copy()
                img_copy.thumbnail((260, 260))
                thumb_buf = io.BytesIO()
                img_copy.save(thumb_buf, format="PNG")
                b64 = base64.b64encode(thumb_buf.getvalue()).decode("ascii")
                return f"data:image/png;base64,{b64}"
    except Exception:
        pass
    return None


def validate_file_content(file_bytes: bytes, filename: str, expected_types: list) -> None:
    """Validates file bytes for emptiness, size, extension, and corrupt headers."""
    if not file_bytes or len(file_bytes) == 0:
        raise ValueError("The uploaded file is empty (0 bytes). Please upload a valid document.")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File size exceeds the {MAX_FILE_SIZE_MB} MB limit ({format_size(len(file_bytes))}). Please upload a smaller file.")

    ext = os.path.splitext(filename)[1].lower().lstrip(".")
    if ext not in expected_types:
        allowed_str = ", ".join(expected_types).upper()
        raise ValueError(f"Unsupported file format (.{ext}). This conversion mode requires: {allowed_str}.")

    # Basic header / magic byte inspection to detect corrupted or mismatched files early
    if ext == "pdf":
        if not file_bytes.startswith(b"%PDF-"):
            raise ValueError("The file is not a valid PDF or the header is corrupted.")
        import pymupdf
        try:
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            if len(doc) == 0:
                doc.close()
                raise ValueError("The PDF file contains no pages.")
            doc.close()
        except Exception as e:
            err_str = str(e).lower()
            if "password" in err_str or "encrypted" in err_str:
                raise ValueError("The PDF is password-protected. Please remove password protection.")
            raise ValueError(f"The PDF file appears corrupted or unreadable ({str(e)}).")

    elif ext == "docx":
        import zipfile
        if not zipfile.is_zipfile(io.BytesIO(file_bytes)):
            raise ValueError("The Word document is corrupted or not a valid .docx package.")

    elif ext in ("jpg", "jpeg", "png"):
        from PIL import Image
        try:
            with Image.open(io.BytesIO(file_bytes)) as img:
                img.verify()
        except Exception as e:
            raise ValueError("The image file appears corrupted or unreadable.")


def convert_pdf_to_docx(pdf_bytes: bytes) -> bytes:
    """Converts PDF bytes to Word (.docx) bytes."""
    temp_pdf_path = None
    temp_docx_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_bytes)
            temp_pdf_path = temp_pdf.name
        temp_docx_path = temp_pdf_path.replace(".pdf", ".docx")

        cv = Converter(temp_pdf_path)
        cv.convert(temp_docx_path)
        cv.close()

        with open(temp_docx_path, "rb") as f:
            return f.read()
    finally:
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except Exception:
                pass
        if temp_docx_path and os.path.exists(temp_docx_path):
            try:
                os.remove(temp_docx_path)
            except Exception:
                pass


def convert_docx_to_pdf(docx_bytes: bytes) -> bytes:
    """
    Converts Word (.docx) bytes to PDF bytes.
    First tries docx2pdf (if MS Word is available on Windows).
    Falls back to mammoth + xhtml2pdf (pure Python) if MS Word is not installed.
    """
    temp_docx_path = None
    temp_pdf_path = None
    try:
        import pythoncom
        from docx2pdf import convert

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
            temp_docx.write(docx_bytes)
            temp_docx_path = temp_docx.name
        temp_pdf_path = temp_docx_path.replace(".docx", ".pdf")

        pythoncom.CoInitialize()
        try:
            convert(temp_docx_path, temp_pdf_path)
            if os.path.exists(temp_pdf_path) and os.path.getsize(temp_pdf_path) > 0:
                with open(temp_pdf_path, "rb") as f:
                    return f.read()
        finally:
            try:
                pythoncom.CoUninitialize()
            except Exception:
                pass
    except Exception:
        # Fallback to pure Python (mammoth + xhtml2pdf)
        import mammoth
        from xhtml2pdf import pisa

        docx_stream = io.BytesIO(docx_bytes)
        result = mammoth.convert_to_html(docx_stream)
        html_body = result.value

        styled_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @page {{
        size: A4;
        margin: 2cm;
    }}
    body {{
        font-family: Helvetica, Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #222222;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #111827;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
    }}
    h1 {{ font-size: 20pt; }}
    h2 {{ font-size: 16pt; }}
    h3 {{ font-size: 13pt; }}
    p {{
        margin-top: 0;
        margin-bottom: 0.8em;
    }}
    table {{
        width: 100%;
        margin-top: 1em;
        margin-bottom: 1em;
    }}
    th, td {{
        border: 1px solid #d1d5db;
        padding: 8px 10px;
        text-align: left;
    }}
    th {{
        background-color: #f3f4f6;
        font-weight: bold;
    }}
    ul, ol {{
        margin-top: 0;
        margin-bottom: 0.8em;
        padding-left: 1.5em;
    }}
    li {{
        margin-bottom: 0.3em;
    }}
</style>
</head>
<body>
    {html_body}
</body>
</html>"""
        pdf_buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(styled_html, dest=pdf_buffer)
        if pisa_status.err:
            raise RuntimeError(f"Could not convert document to PDF (code {pisa_status.err})")
        return pdf_buffer.getvalue()
    finally:
        if temp_docx_path and os.path.exists(temp_docx_path):
            try:
                os.remove(temp_docx_path)
            except Exception:
                pass
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except Exception:
                pass


def convert_images_to_pdf(image_bytes: bytes, filename: str) -> bytes:
    """Converts a JPG or PNG image to PDF bytes using Pillow."""
    from PIL import Image
    img_stream = io.BytesIO(image_bytes)
    img = Image.open(img_stream).convert("RGB")
    pdf_buffer = io.BytesIO()
    img.save(pdf_buffer, format="PDF", resolution=150)
    return pdf_buffer.getvalue()


def convert_pdf_to_images(pdf_bytes: bytes, fmt: str = "jpg") -> list:
    """
    Converts each page of a PDF to an image.
    Returns list of (filename, bytes) tuples.
    fmt: 'jpg' or 'png'
    """
    import pymupdf  # fitz
    pil_fmt = "JPEG" if fmt == "jpg" else "PNG"
    mime_ext = ".jpg" if fmt == "jpg" else ".png"
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    results = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        mat = pymupdf.Matrix(2.0, 2.0)  # 2x zoom → ~144 dpi
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_bytes = pix.tobytes(pil_fmt.lower())
        results.append((f"page_{page_num + 1}{mime_ext}", img_bytes))
    doc.close()
    return results


def convert_pdf_to_excel(pdf_bytes: bytes) -> bytes:
    """
    Converts PDF to an Excel workbook (.xlsx).
    Extracts tabular data using PyMuPDF table detection.
    If no formal tables are detected, extracts lines cleanly structured by page.
    """
    import pymupdf
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    if len(doc) == 0:
        doc.close()
        raise ValueError("The provided PDF file has no pages.")

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="429EC2")
    cell_font = Font(name="Calibri", size=10, color="000000")
    thin_border = Border(
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
        top=Side(style="thin", color="CBD5E1"),
        bottom=Side(style="thin", color="CBD5E1")
    )

    total_extracted_rows = 0

    for page_idx, page in enumerate(doc):
        sheet_title = f"Page {page_idx + 1}"[:31]
        ws = wb.create_sheet(title=sheet_title)

        # First try table detection
        tables_found = False
        try:
            tabs = page.find_tables()
            if tabs and len(tabs.tables) > 0:
                current_row = 1
                for t_idx, tab in enumerate(tabs):
                    if t_idx > 0:
                        current_row += 2  # spacing between tables
                    data = tab.extract()
                    for r_idx, row in enumerate(data):
                        clean_row = [str(cell).strip() if cell is not None else "" for cell in row]
                        ws.append(clean_row)
                        for col_idx in range(1, len(clean_row) + 1):
                            cell = ws.cell(row=current_row, column=col_idx)
                            cell.border = thin_border
                            if r_idx == 0:
                                cell.fill = header_fill
                                cell.font = header_font
                            else:
                                cell.font = cell_font
                        current_row += 1
                        total_extracted_rows += 1
                tables_found = True
        except Exception:
            tables_found = False

        if not tables_found:
            # Fallback: extract structured text blocks & lines cleanly
            text = page.get_text("text").strip()
            if text:
                ws.append(["Line #", "Extracted Content"])
                for col_idx in (1, 2):
                    c = ws.cell(row=1, column=col_idx)
                    c.fill = header_fill
                    c.font = header_font
                    c.border = thin_border

                row_counter = 2
                for line_idx, line in enumerate(text.splitlines(), start=1):
                    clean_line = line.strip()
                    if clean_line:
                        # If line contains multiple spaces or tabs, split into columns
                        if "\t" in clean_line:
                            parts = [p.strip() for p in clean_line.split("\t")]
                            ws.append([line_idx] + parts)
                        else:
                            ws.append([line_idx, clean_line])

                        for col_idx in range(1, ws.max_column + 1):
                            c = ws.cell(row=row_counter, column=col_idx)
                            c.font = cell_font
                            c.border = thin_border
                        row_counter += 1
                        total_extracted_rows += 1
            else:
                ws.append(["Notice", "No text or tables detected on this page (page may contain scanned images only)."])

        # Auto-adjust column widths
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or "")
                if len(val) > max_len:
                    max_len = len(val)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 60)

    doc.close()

    if total_extracted_rows == 0:
        raise ValueError("Could not extract any tabular data or readable text from this PDF. It may be scanned or empty.")

    output_stream = io.BytesIO()
    wb.save(output_stream)
    return output_stream.getvalue()


def convert_pdf_to_pptx(pdf_bytes: bytes) -> bytes:
    """
    Converts PDF pages into a PowerPoint presentation (.pptx).
    Each page is rendered as a sharp high-resolution slide visual with matching dimensions.
    """
    import pymupdf
    import pptx
    from pptx.util import Inches

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    if len(doc) == 0:
        doc.close()
        raise ValueError("The provided PDF file has no pages.")

    prs = pptx.Presentation()
    # Blank slide layout (layout index 6 is blank in standard template)
    blank_layout = prs.slide_layouts[6]

    for page_idx, page in enumerate(doc):
        # Determine page aspect ratio
        rect = page.rect
        w_pts = rect.width
        h_pts = rect.height

        # Set presentation slide size to match the first page's aspect ratio
        if page_idx == 0:
            prs.slide_width = Inches(w_pts / 72.0)
            prs.slide_height = Inches(h_pts / 72.0)

        # Render page at 2x resolution (144 dpi) for crisp projection/reading
        mat = pymupdf.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_bytes = pix.tobytes("png")

        slide = prs.slides.add_slide(blank_layout)
        img_stream = io.BytesIO(img_bytes)
        slide.shapes.add_picture(img_stream, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

    doc.close()

    output_stream = io.BytesIO()
    prs.save(output_stream)
    return output_stream.getvalue()


def convert_pdf_to_txt(pdf_bytes: bytes) -> bytes:
    """
    Extracts text from each PDF page into clean, formatted UTF-8 plain text (.txt).
    """
    import pymupdf

    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    if len(doc) == 0:
        doc.close()
        raise ValueError("The provided PDF file has no pages.")

    page_texts = []
    has_text = False

    for page_idx, page in enumerate(doc):
        text = page.get_text("text").strip()
        if text:
            has_text = True
            page_texts.append(f"--- Page {page_idx + 1} ---\n\n{text}")
        else:
            page_texts.append(f"--- Page {page_idx + 1} ---\n\n[No text detected on this page]")

    doc.close()

    if not has_text:
        raise ValueError("No extractable text was found in this PDF. It may consist entirely of scanned images.")

    full_text = "\n\n" + ("\n\n" + "=" * 40 + "\n\n").join(page_texts) + "\n"
    return full_text.strip().encode("utf-8")


# ---------------------------------------------------------
# PDF Tools Logic
# ---------------------------------------------------------
def merge_pdfs(pdf_bytes_list: list) -> bytes:
    import pymupdf
    import io
    doc_out = pymupdf.open()
    for p_bytes in pdf_bytes_list:
        doc = pymupdf.open(stream=p_bytes, filetype="pdf")
        doc_out.insert_pdf(doc)
    
    output_stream = io.BytesIO()
    doc_out.save(output_stream)
    doc_out.close()
    return output_stream.getvalue()

def split_pdf(pdf_bytes: bytes, pages_str: str) -> bytes:
    import pymupdf
    import io
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages_to_keep = []
    parts = pages_str.replace(" ", "").split(",")
    for p in parts:
        if "-" in p:
            start, end = p.split("-")
            pages_to_keep.extend(range(int(start) - 1, int(end)))
        else:
            if p:
                pages_to_keep.append(int(p) - 1)
    
    doc.select(pages_to_keep)
    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    return output_stream.getvalue()

def compress_pdf(pdf_bytes: bytes, level: str) -> bytes:
    import pymupdf
    import io
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    output_stream = io.BytesIO()
    
    if level == "Low":
        doc.save(output_stream, deflate=True)
    elif level == "Medium":
        doc.save(output_stream, garbage=3, deflate=True)
    else: # High
        doc.save(output_stream, garbage=4, deflate=True)
    doc.close()
    return output_stream.getvalue()

def rotate_pdf(pdf_bytes: bytes, angle: int) -> bytes:
    import pymupdf
    import io
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        page.set_rotation(angle)
    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    return output_stream.getvalue()

def protect_pdf(pdf_bytes: bytes, password: str) -> bytes:
    import pymupdf
    import io
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    output_stream = io.BytesIO()
    doc.save(output_stream, encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw=password, owner_pw=password)
    doc.close()
    return output_stream.getvalue()

# ---------------------------------------------------------
# State Management
# ---------------------------------------------------------
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0
if "converted_data" not in st.session_state:
    st.session_state["converted_data"] = None
if "output_filename" not in st.session_state:
    st.session_state["output_filename"] = None
if "conversion_error" not in st.session_state:
    st.session_state["conversion_error"] = None
if "multi_files" not in st.session_state:
    st.session_state["multi_files"] = None
if "pdf_img_fmt" not in st.session_state:
    st.session_state["pdf_img_fmt"] = "jpg"
if "recent_conversions" not in st.session_state:
    st.session_state["recent_conversions"] = []

# App Header with Modern SVG Icon, Title, Subtitle, and Trust Badges
st.markdown("""
<div class="app-header">
    <div class="app-header-icon">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V8L14 2Z" stroke="#429ec2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M14 2V8H20" stroke="#83bd64" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 15L12 12M12 12L15 15M12 12V18" stroke="#83bd64" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <h1 class="app-header-title">Multi-Format Converter</h1>
    </div>
</div>
<div class="app-header-subtitle">Convert documents & images quickly and securely.</div>
<div class="trust-badge-bar">
    <span class="trust-item"><span class="trust-dot blue"></span>Local Processing</span>
    <span class="trust-divider">•</span>
    <span class="trust-item"><span class="trust-dot green"></span>Fast Conversion</span>
    <span class="trust-divider">•</span>
    <span class="trust-item"><span class="trust-dot blue"></span>Privacy First</span>
</div>
""", unsafe_allow_html=True)

# Conversion Selector
st.markdown('<div class="section-label" style="text-align: center; margin-bottom: 1rem; margin-top: 1rem;">APP MODE</div>', unsafe_allow_html=True)
app_mode = st.radio(
    label="App Mode",
    options=["🔄 Converter", "🛠️ PDF Tools"],
    horizontal=True,
    label_visibility="collapsed",
    key="app_mode"
)

if app_mode == "🔄 Converter":
    st.markdown('<div class="section-label" style="text-align: center; margin-bottom: 1rem; margin-top: 1rem;">CONVERTER TOOLS</div>', unsafe_allow_html=True)
    conversion_option = st.radio(
        label="Conversion Mode",
        options=[PDF_TO_WORD, WORD_TO_PDF, IMG_TO_PDF, PDF_TO_IMG, PDF_TO_EXCEL, PDF_TO_PPTX, PDF_TO_TXT],
        horizontal=True,
        label_visibility="collapsed",
        key="selected_mode"
    )
    is_tool_mode = False
else:
    st.markdown('<div class="section-label" style="text-align: center; margin-bottom: 1rem; margin-top: 1rem;">PDF TOOLS</div>', unsafe_allow_html=True)
    conversion_option = st.radio(
        label="PDF Tool",
        options=["🔗 Merge PDF", "✂️ Split PDF", "📦 Compress PDF", "🔄 Rotate PDF", "🔐 Password Protect"],
        horizontal=True,
        label_visibility="collapsed",
        key="selected_tool"
    )
    is_tool_mode = True

if not is_tool_mode and conversion_option == PDF_TO_WORD:
    file_type_title = "PDF"
    allowed_types = ["pdf"]
    download_label = "Download Word Document"
    download_mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    output_ext = ".docx"
    doc_icon = "📄"
    icon_color_class = ""
elif conversion_option == WORD_TO_PDF:
    file_type_title = "Word (.docx)"
    allowed_types = ["docx"]
    download_label = "Download PDF Document"
    download_mime = "application/pdf"
    output_ext = ".pdf"
    doc_icon = "📝"
    icon_color_class = "green"
elif conversion_option == IMG_TO_PDF:
    file_type_title = "Image (JPG / PNG)"
    allowed_types = ["jpg", "jpeg", "png"]
    download_label = "Download PDF"
    download_mime = "application/pdf"
    output_ext = ".pdf"
    doc_icon = "🖼️"
    icon_color_class = "green"
elif conversion_option == PDF_TO_IMG:
    file_type_title = "PDF"
    allowed_types = ["pdf"]
    download_label = "Download Images (ZIP)"
    download_mime = "application/zip"
    output_ext = ".zip"
    doc_icon = "🔍"
    icon_color_class = ""
elif conversion_option == PDF_TO_EXCEL:
    file_type_title = "PDF"
    allowed_types = ["pdf"]
    download_label = "Download Excel Spreadsheet"
    download_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    output_ext = ".xlsx"
    doc_icon = "📊"
    icon_color_class = "green"
elif conversion_option == PDF_TO_PPTX:
    file_type_title = "PDF"
    allowed_types = ["pdf"]
    download_label = "Download PowerPoint Presentation"
    download_mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    output_ext = ".pptx"
    doc_icon = "📽️"
    icon_color_class = ""
elif not is_tool_mode:  # PDF_TO_TXT
    file_type_title = "PDF"
    allowed_types = ["pdf"]
    download_label = "Download Text File"
    download_mime = "text/plain"
    output_ext = ".txt"
    doc_icon = "📃"
    icon_color_class = "green"
else:
    file_type_title = "PDF"
    allowed_types = ["pdf"]
    download_mime = "application/pdf"
    output_ext = ".pdf"
    doc_icon = "📄"
    icon_color_class = ""
    
    if conversion_option == "🔗 Merge PDF":
        download_label = "Download Merged PDF"
    elif conversion_option == "✂️ Split PDF":
        download_label = "Download Split PDF"
    elif conversion_option == "📦 Compress PDF":
        download_label = "Download Compressed PDF"
    elif conversion_option == "🔄 Rotate PDF":
        download_label = "Download Rotated PDF"
    elif conversion_option == "🔐 Password Protect":
        download_label = "Download Protected PDF"

# Specific tool inputs
if is_tool_mode:
    if conversion_option == "✂️ Split PDF":
        st.session_state["split_pages"] = st.text_input("Pages to extract (e.g. 1-3, 5)", "1")
    elif conversion_option == "📦 Compress PDF":
        st.session_state["compress_level"] = st.selectbox("Compression Level", ["Low", "Medium", "High"])
    elif conversion_option == "🔄 Rotate PDF":
        st.session_state["rotate_angle"] = st.selectbox("Rotation Angle", [90, 180, 270])
    elif conversion_option == "🔐 Password Protect":
        st.session_state["pdf_password"] = st.text_input("Password", type="password")

# For PDF → Image: let user pick JPG or PNG before uploading
if conversion_option == PDF_TO_IMG:
    fmt_col1, fmt_col2 = st.columns([1, 1], gap="small")
    with fmt_col1:
        if st.button("JPG format",
                     type="primary" if st.session_state["pdf_img_fmt"] == "jpg" else "secondary",
                     use_container_width=True, key="fmt_jpg_btn"):
            st.session_state["pdf_img_fmt"] = "jpg"
            st.session_state["converted_data"] = None
            st.rerun()
    with fmt_col2:
        if st.button("PNG format",
                     type="primary" if st.session_state["pdf_img_fmt"] == "png" else "secondary",
                     use_container_width=True, key="fmt_png_btn"):
            st.session_state["pdf_img_fmt"] = "png"
            st.session_state["converted_data"] = None
            st.rerun()
    fmt_label = st.session_state["pdf_img_fmt"].upper()
    download_label = f"Download {fmt_label} Images (ZIP)"
    download_mime = f"image/{st.session_state['pdf_img_fmt']}"

# Native Upload Area without redundant duplicate labels
accept_multiple = (is_tool_mode and conversion_option == "🔗 Merge PDF")

uploaded_file = st.file_uploader(
    label="Choose a file",
    type=allowed_types,
    accept_multiple_files=accept_multiple,
    label_visibility="collapsed",
    key=f"file_uploader_{st.session_state['uploader_key']}"
)

# Detect change in uploaded file or mode to reset state
if isinstance(uploaded_file, list):
    file_names = "_".join([f.name for f in uploaded_file])
elif uploaded_file:
    file_names = uploaded_file.name
else:
    file_names = None
current_state_key = f"{conversion_option}_{file_names}"
if st.session_state.get("last_state_key") != current_state_key:
    st.session_state["last_state_key"] = current_state_key
    st.session_state["converted_data"] = None
    st.session_state["output_filename"] = None
    st.session_state["conversion_error"] = None
    st.session_state["multi_files"] = None

# Empty State chips when no file is uploaded yet
if not uploaded_file:
    type_chips = "".join([f'<span class="upload-empty-chip">.{t.upper()}</span>' for t in allowed_types])
    st.markdown(f"""
    <div class="upload-empty-footer">
        <span style="font-weight:600;color:#94a3b8;">Supported formats:</span>
        {type_chips}
        <span style="color:#64748b;">• Max {MAX_FILE_SIZE_MB}MB</span>
    </div>
    """, unsafe_allow_html=True)

# If file is uploaded, show the File Preview card & thumbnails
if uploaded_file:
    files_to_preview = uploaded_file if isinstance(uploaded_file, list) else [uploaded_file]
    for idx, f in enumerate(files_to_preview):
        f_bytes = f.getvalue()
        f_meta = get_file_metadata(f_bytes, f.name)
        thumb_uri = generate_thumbnail(f_bytes, f.name)

        # Meta pills
        meta_pills = [f'<span class="file-preview-meta-pill">{f_meta["type_label"]}</span>', f'<span>{f_meta["size_str"]}</span>']
        if f_meta["page_count"] is not None:
            pages_word = "page" if f_meta["page_count"] == 1 else "pages"
            meta_pills.append(f'<span class="file-preview-meta-pill">📄 {f_meta["page_count"]} {pages_word}</span>')
        elif f_meta["dimensions"] is not None:
            meta_pills.append(f'<span class="file-preview-meta-pill">📐 {f_meta["dimensions"]}</span>')

        pills_html = " • ".join(meta_pills)

        # Left icon or thumbnail
        if thumb_uri:
            icon_html = f'<img src="{thumb_uri}" class="file-thumbnail-img" alt="Thumbnail" />'
        else:
            icon_html = f'<div class="file-preview-icon {icon_color_class}">{doc_icon}</div>'

        card_col1, card_col2 = st.columns([4.2, 0.8], gap="small")
        with card_col1:
            st.markdown(f"""
            <div class="file-preview-card">
                <div class="file-preview-left">
                    {icon_html}
                    <div class="file-preview-details">
                        <span class="file-preview-name" title="{f.name}">{f.name}</span>
                        <div class="file-preview-meta">
                            {pills_html}
                        </div>
                    </div>
                </div>
                <span class="file-preview-badge">✓ Ready</span>
            </div>
            """, unsafe_allow_html=True)
        with card_col2:
            st.markdown('<div style="height: 6px;"></div>', unsafe_allow_html=True)
            if st.button("🗑️ Remove", key=f"remove_file_{idx}_{st.session_state['uploader_key']}", use_container_width=True, help="Remove file"):
                st.session_state["converted_data"] = None
                st.session_state["output_filename"] = None
                st.session_state["conversion_error"] = None
                st.session_state["uploader_key"] += 1
                st.rerun()

        # Visual preview modal-like card for single file
        if thumb_uri and not isinstance(uploaded_file, list):
            f_ext = os.path.splitext(f.name)[1].lower().lstrip(".")
            caption_text = f"First page preview ({f_meta['page_count']} pages total)" if f_ext == "pdf" and f_meta.get("page_count") else "Image preview"
            st.markdown(f"""
            <div class="file-visual-preview-box">
                <img src="{thumb_uri}" alt="Preview" />
                <span class="file-visual-preview-caption">{caption_text}</span>
            </div>
            """, unsafe_allow_html=True)

# Action Buttons (Convert & Clear)
action_btn_label = "Process Document" if is_tool_mode else "Convert Document"
if not uploaded_file:
    st.button(action_btn_label, disabled=True, use_container_width=True, key="convert_btn_disabled")
else:
    btn_col1, btn_col2 = st.columns([3.6, 1.4], gap="small")
    with btn_col1:
        convert_clicked = st.button(action_btn_label, type="primary", use_container_width=True, key="convert_btn_active")
    with btn_col2:
        clear_clicked = st.button("Clear", type="secondary", use_container_width=True, key="clear_btn_active")

    if clear_clicked:
        st.session_state["converted_data"] = None
        st.session_state["output_filename"] = None
        st.session_state["conversion_error"] = None
        st.session_state["uploader_key"] += 1
        st.rerun()

    if convert_clicked:
        st.session_state["conversion_error"] = None
        
        # Professional progressive state container
        progress_placeholder = st.empty()
        
        def render_progress(step_text: str, percent: int):
            progress_placeholder.markdown(f"""
            <div class="progress-box">
                <div class="progress-header">
                    <span class="progress-title-left">
                        <span style="color:#429ec2;">⚡</span>
                        <span>{step_text}</span>
                    </span>
                    <span class="progress-percent">{percent}%</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: {percent}%;"></div>
                </div>
                <div class="progress-step-text">
                    <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:#83bd64;"></span>
                    <span>Safe local client processing</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        try:
            render_progress("Preparing file...", 15)
            
            if is_tool_mode and conversion_option == "🔗 Merge PDF":
                if len(uploaded_file) < 2:
                    raise ValueError("Please upload at least two PDFs to merge.")
                file_bytes_list = []
                for f in uploaded_file:
                    b = f.getvalue()
                    validate_file_content(b, f.name, allowed_types)
                    file_bytes_list.append(b)
                base_name = "merged_document"
                orig_display_name = f"{len(uploaded_file)} PDF files"
            else:
                file_bytes = uploaded_file.getvalue()
                validate_file_content(file_bytes, uploaded_file.name, allowed_types)
                base_name = os.path.splitext(uploaded_file.name)[0]
                orig_display_name = uploaded_file.name

            render_progress("Converting document...", 55)

            if is_tool_mode:
                if conversion_option == "🔗 Merge PDF":
                    converted_bytes = merge_pdfs(file_bytes_list)
                    st.session_state["output_filename"] = f"{base_name}.pdf"
                elif conversion_option == "✂️ Split PDF":
                    converted_bytes = split_pdf(file_bytes, st.session_state["split_pages"])
                    st.session_state["output_filename"] = f"{base_name}_split.pdf"
                elif conversion_option == "📦 Compress PDF":
                    converted_bytes = compress_pdf(file_bytes, st.session_state["compress_level"])
                    st.session_state["output_filename"] = f"{base_name}_compressed.pdf"
                elif conversion_option == "🔄 Rotate PDF":
                    converted_bytes = rotate_pdf(file_bytes, st.session_state["rotate_angle"])
                    st.session_state["output_filename"] = f"{base_name}_rotated.pdf"
                elif conversion_option == "🔐 Password Protect":
                    if not st.session_state.get("pdf_password"):
                        raise ValueError("Password cannot be empty.")
                    converted_bytes = protect_pdf(file_bytes, st.session_state["pdf_password"])
                    st.session_state["output_filename"] = f"{base_name}_protected.pdf"
                
                st.session_state["converted_data"] = converted_bytes
                st.session_state["multi_files"] = None
            
            elif not is_tool_mode and conversion_option == PDF_TO_WORD:
                converted_bytes = convert_pdf_to_docx(file_bytes)
                st.session_state["converted_data"] = converted_bytes
                st.session_state["output_filename"] = f"{base_name}.docx"
                st.session_state["multi_files"] = None

            elif conversion_option == WORD_TO_PDF:
                converted_bytes = convert_docx_to_pdf(file_bytes)
                st.session_state["converted_data"] = converted_bytes
                st.session_state["output_filename"] = f"{base_name}.pdf"
                st.session_state["multi_files"] = None

            elif conversion_option == IMG_TO_PDF:
                converted_bytes = convert_images_to_pdf(file_bytes, uploaded_file.name)
                st.session_state["converted_data"] = converted_bytes
                st.session_state["output_filename"] = f"{base_name}.pdf"
                st.session_state["multi_files"] = None

            elif conversion_option == PDF_TO_IMG:
                # Determine requested format from a session flag (default jpg)
                img_fmt = st.session_state.get("pdf_img_fmt", "jpg")
                pages = convert_pdf_to_images(file_bytes, fmt=img_fmt)
                if len(pages) == 1:
                    # Single page – download directly
                    st.session_state["converted_data"] = pages[0][1]
                    st.session_state["output_filename"] = f"{base_name}{pages[0][0][6:]}"  # strip 'page_1'
                    st.session_state["multi_files"] = None
                else:
                    # Multiple pages – zip them
                    import zipfile
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                        for fname, fbytes in pages:
                            zf.writestr(f"{base_name}_{fname}", fbytes)
                    st.session_state["converted_data"] = zip_buffer.getvalue()
                    st.session_state["output_filename"] = f"{base_name}_images.zip"
                    st.session_state["multi_files"] = [(f"{base_name}_{fn}", fb) for fn, fb in pages]

            elif conversion_option == PDF_TO_EXCEL:
                converted_bytes = convert_pdf_to_excel(file_bytes)
                st.session_state["converted_data"] = converted_bytes
                st.session_state["output_filename"] = f"{base_name}.xlsx"
                st.session_state["multi_files"] = None

            elif conversion_option == PDF_TO_PPTX:
                converted_bytes = convert_pdf_to_pptx(file_bytes)
                st.session_state["converted_data"] = converted_bytes
                st.session_state["output_filename"] = f"{base_name}.pptx"
                st.session_state["multi_files"] = None

            elif conversion_option == PDF_TO_TXT:
                converted_bytes = convert_pdf_to_txt(file_bytes)
                st.session_state["converted_data"] = converted_bytes
                st.session_state["output_filename"] = f"{base_name}.txt"
                st.session_state["multi_files"] = None

            render_progress("Almost done...", 90)

            # Record in recent conversions (current browser session only)
            if "recent_conversions" not in st.session_state:
                st.session_state["recent_conversions"] = []
            
            recent_entry = {
                "type": conversion_option,
                "orig": orig_display_name,
                "output": st.session_state.get("output_filename", "output")
            }
            # Avoid duplicate consecutive entries
            if not st.session_state["recent_conversions"] or st.session_state["recent_conversions"][0] != recent_entry:
                st.session_state["recent_conversions"].insert(0, recent_entry)
                # Keep last 8 items
                st.session_state["recent_conversions"] = st.session_state["recent_conversions"][:8]

            render_progress("Conversion complete!", 100)
            progress_placeholder.empty()

        except ValueError as ve:
            progress_placeholder.empty()
            st.session_state["conversion_error"] = str(ve)
        except Exception as e:
            progress_placeholder.empty()
            err_msg = str(e)
            if "password" in err_msg.lower() or "encrypted" in err_msg.lower():
                st.session_state["conversion_error"] = "The file is password-protected. Please remove the password and try again."
            elif "corrupt" in err_msg.lower() or "invalid" in err_msg.lower() or "damaged" in err_msg.lower():
                st.session_state["conversion_error"] = "The file appears to be corrupted or invalid. Please check the file and try again."
            elif "no extractable text" in err_msg.lower() or "could not extract" in err_msg.lower():
                st.session_state["conversion_error"] = f"{err_msg} (If this is a scanned document without OCR text, consider using PDF → Image instead)."
            else:
                st.session_state["conversion_error"] = f"Unable to convert document. Please verify the file is a valid {allowed_types[0].upper()} and try again."

# Display Error State Card if any
if st.session_state.get("conversion_error"):
    st.markdown(f"""
    <div class="error-card">
        <div class="error-card-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 9V13M12 17H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Conversion Failed</span>
        </div>
        <div class="error-card-desc">{st.session_state['conversion_error']}</div>
    </div>
    """, unsafe_allow_html=True)

# Display Success Result Card & Prominent Download Area
if st.session_state.get("converted_data") is not None:
    output_size_formatted = format_size(len(st.session_state["converted_data"]))
    out_name = st.session_state.get("output_filename", "output")
    if output_ext == ".docx":
        out_icon = "📝"
    elif output_ext in (".jpg", ".png", ".zip"):
        out_icon = "🖼️"
    elif output_ext == ".xlsx":
        out_icon = "📊"
    elif output_ext == ".pptx":
        out_icon = "📽️"
    elif output_ext == ".txt":
        out_icon = "📃"
    else:
        out_icon = "📄"

    st.markdown(f"""
    <div class="success-card">
        <div class="success-header">
            <span class="success-icon-badge">✓</span>
            <span class="success-title">Conversion Complete!</span>
        </div>
        <div class="success-desc">Your output document is ready for instant download.</div>
        <div class="success-meta">
            <span>{out_icon}</span>
            <b>{out_name}</b>
            <span>•</span>
            <span>{output_size_formatted}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # PDF → Image with multiple pages: also show individual page downloads
    multi_files = st.session_state.get("multi_files")
    if multi_files and len(multi_files) > 1:
        st.markdown('<div class="section-label" style="margin-top:0.8rem;">Individual Pages</div>', unsafe_allow_html=True)
        for pg_name, pg_bytes in multi_files:
            st.download_button(
                label=f"⬇️ {pg_name}",
                data=pg_bytes,
                file_name=pg_name,
                mime="image/jpeg" if pg_name.endswith(".jpg") else "image/png",
                use_container_width=True,
                key=f"dl_{pg_name}"
            )
        st.markdown("<hr style='border-color:rgba(66,158,194,0.15);margin:0.6rem 0;'>", unsafe_allow_html=True)

    # Prominent Download and Clear Action row
    dl_col1, dl_col2 = st.columns([3.8, 1.2], gap="small")
    with dl_col1:
        st.download_button(
            label=f"⬇️ {download_label} ({output_size_formatted})",
            data=st.session_state["converted_data"],
            file_name=out_name,
            mime=download_mime,
            use_container_width=True,
            key="primary_download_btn"
        )
    with dl_col2:
        if st.button("Clear File", key="clear_result_btn", type="secondary", use_container_width=True):
            st.session_state["converted_data"] = None
            st.session_state["output_filename"] = None
            st.session_state["conversion_error"] = None
            st.session_state["uploader_key"] += 1
            st.rerun()

# ---------------------------------------------------------
# Recent Conversions (Current Session Only)
# ---------------------------------------------------------
if st.session_state.get("recent_conversions"):
    st.markdown("""
    <div class="recent-section">
        <div class="section-label" style="justify-content: flex-start; gap: 0.4rem; margin-bottom: 0.75rem;">
            <span>🕒</span>
            <span>Recent Conversions (This Session)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for item in st.session_state["recent_conversions"]:
        st.markdown(f"""
        <div class="recent-item">
            <div class="recent-item-left">
                <span class="recent-type-badge">{item['type']}</span>
                <div class="recent-filenames">
                    <span class="recent-orig-name" title="{item['orig']}">Source: {item['orig']}</span>
                    <span class="recent-out-name" title="{item['output']}">Output: {item['output']}</span>
                </div>
            </div>
            <span class="recent-time">Completed</span>
        </div>
        """, unsafe_allow_html=True)

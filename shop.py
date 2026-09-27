from flask import Flask, jsonify, render_template_string, request, session, redirect, url_for
import os
import json

app = Flask(__name__)
app.secret_key = "jajmia-secret-key-2026-mahim1432"

# ==================== দোকানের তথ্য ====================
SHOP_NAME = "জজ মিয়া স্টোর"
SHOP_ADDRESS = "কীর্তনীয়া গ্রাম, ঝরনা ঘাট বাজার, কাপাসিয়া, গাজীপুর, বাংলাদেশ"

# ==================== Admin Password ====================
ADMIN_PASSWORD = "mahim1432"

# ==================== Data File ====================
DATA_FILE = "products_data.json"

# ==================== Default Products ====================
DEFAULT_PRODUCTS = [
    {"id": 1,  "name": "চাল",         "price": 70,  "unit": "কেজি",    "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400", "category": "মুদি"},
    {"id": 2,  "name": "ডাল",         "price": 120, "unit": "কেজি",    "image": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=400", "category": "মুদি"},
    {"id": 3,  "name": "চিনি",        "price": 130, "unit": "কেজি",    "image": "https://images.unsplash.com/photo-1581441363689-1f3c3c414635?w=400", "category": "মুদি"},
    {"id": 4,  "name": "লবণ",         "price": 40,  "unit": "কেজি",    "image": "https://images.unsplash.com/photo-1518110925495-b37e912adecb?w=400", "category": "মুদি"},
    {"id": 5,  "name": "তেল",         "price": 180, "unit": "লিটার",   "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400", "category": "মুদি"},
    {"id": 6,  "name": "আটা",         "price": 60,  "unit": "কেজি",    "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400", "category": "মুদি"},
    {"id": 7,  "name": "ময়দা",        "price": 65,  "unit": "কেজি",    "image": "https://images.unsplash.com/photo-1568254183919-78a4f43a2877?w=400", "category": "মুদি"},
    {"id": 8,  "name": "চা",          "price": 90,  "unit": "প্যাকেট", "image": "https://images.unsplash.com/photo-1597318181409-cf64d0b5d8a2?w=400", "category": "পানীয়"},
    {"id": 9,  "name": "বিস্কুট",     "price": 25,  "unit": "প্যাকেট", "image": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400", "category": "স্ন্যাকস"},
    {"id": 10, "name": "চানাচুর",     "price": 20,  "unit": "প্যাকেট", "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400", "category": "স্ন্যাকস"},
    {"id": 11, "name": "চিপস",        "price": 20,  "unit": "প্যাকেট", "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=400", "category": "স্ন্যাকস"},
    {"id": 12, "name": "চকলেট",       "price": 15,  "unit": "পিস",     "image": "https://images.unsplash.com/photo-1511381939415-e44015466834?w=400", "category": "মিষ্টি"},
    {"id": 13, "name": "ক্যান্ডি",    "price": 5,   "unit": "পিস",     "image": "https://images.unsplash.com/photo-1582058091505-f87a2e55a40f?w=400", "category": "মিষ্টি"},
    {"id": 14, "name": "জুস",         "price": 35,  "unit": "বোতল",    "image": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400", "category": "পানীয়"},
    {"id": 15, "name": "পানি",        "price": 15,  "unit": "বোতল",    "image": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400", "category": "পানীয়"},
    {"id": 16, "name": "সাবান",       "price": 30,  "unit": "পিস",     "image": "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?w=400", "category": "প্রসাধনী"},
    {"id": 17, "name": "শ্যাম্পু",    "price": 90,  "unit": "বোতল",    "image": "https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=400", "category": "প্রসাধনী"},
    {"id": 18, "name": "টুথপেস্ট",    "price": 75,  "unit": "পিস",     "image": "https://images.unsplash.com/photo-1559304787-945aa4341065?w=400", "category": "প্রসাধনী"},
    {"id": 19, "name": "ডিটারজেন্ট",  "price": 55,  "unit": "প্যাকেট", "image": "https://images.unsplash.com/photo-1585421514738-01798e348b17?w=400", "category": "প্রসাধনী"},
]

# ==================== Load & Save Data ====================
def load_products():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_PRODUCTS.copy()
    return DEFAULT_PRODUCTS.copy()

def save_products(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if not os.path.exists(DATA_FILE):
    save_products(DEFAULT_PRODUCTS)

def get_categories(products):
    cats = []
    for p in products:
        if p.get("category") and p["category"] not in cats:
            cats.append(p["category"])
    return cats

def is_logged_in():
    return session.get("admin_logged_in", False)

# ==================== Customer HTML ====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ shop_name }} — প্রিমিয়াম স্টোর</title>
    <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #0f5132; --primary-light: #198754; --primary-dark: #0a3622;
            --accent: #ffc107; --bg: #f4f7f5; --card-bg: #ffffff;
            --text: #1a1a1a; --text-muted: #6c757d; --border: #e0e6e2;
            --shadow-sm: 0 2px 8px rgba(15, 81, 50, 0.06);
            --shadow-md: 0 8px 24px rgba(15, 81, 50, 0.10);
            --shadow-lg: 0 16px 48px rgba(15, 81, 50, 0.18);
            --shadow-glow: 0 0 40px rgba(25, 135, 84, 0.35);
            --radius: 16px; --radius-sm: 10px;
            --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }
        html { scroll-behavior: smooth; }
        body {
            font-family: 'Hind Siliguri', 'Poppins', sans-serif;
            background: var(--bg); color: var(--text);
            line-height: 1.6; overflow-x: hidden; min-height: 100vh;
        }
        .bg-shapes { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; overflow: hidden; pointer-events: none; }
        .bg-shapes .shape { position: absolute; border-radius: 50%; filter: blur(80px); opacity: 0.15; animation: floatShape 20s infinite ease-in-out; }
        .bg-shapes .shape:nth-child(1) { width: 400px; height: 400px; background: #198754; top: -100px; left: -100px; }
        .bg-shapes .shape:nth-child(2) { width: 350px; height: 350px; background: #ffc107; top: 40%; right: -100px; animation-delay: 5s; }
        .bg-shapes .shape:nth-child(3) { width: 300px; height: 300px; background: #20c997; bottom: -100px; left: 30%; animation-delay: 10s; }
        @keyframes floatShape {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(60px, -40px) scale(1.1); }
            66% { transform: translate(-40px, 60px) scale(0.95); }
        }
        header {
            position: relative;
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, #20c997 100%);
            background-size: 200% 200%;
            animation: gradientShift 12s ease infinite;
            color: white; padding: 50px 20px 70px; text-align: center;
            overflow: hidden; box-shadow: var(--shadow-md);
        }
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        header::before {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.12) 0%, transparent 40%),
                              radial-gradient(circle at 80% 70%, rgba(255,255,255,0.08) 0%, transparent 40%);
            pointer-events: none;
        }
        header::after {
            content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 60px;
            background: var(--bg); clip-path: ellipse(75% 100% at 50% 100%);
        }
        .header-content { position: relative; z-index: 2; max-width: 1200px; margin: 0 auto; }
        .logo-badge {
            display: inline-flex; align-items: center; justify-content: center;
            width: 80px; height: 80px; border-radius: 50%;
            background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);
            border: 2px solid rgba(255,255,255,0.3); margin-bottom: 18px; font-size: 2.2rem;
            animation: bounceIn 1s ease, pulseGlow 3s ease-in-out infinite 1s;
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 0 0 rgba(255,255,255,0.4); }
            50% { box-shadow: 0 0 0 20px rgba(255,255,255,0); }
        }
        @keyframes bounceIn {
            0% { transform: scale(0) rotate(-180deg); opacity: 0; }
            60% { transform: scale(1.2) rotate(10deg); opacity: 1; }
            100% { transform: scale(1) rotate(0); }
        }
        header h1 {
            font-family: 'Poppins', 'Hind Siliguri', sans-serif;
            font-size: clamp(1.8rem, 5vw, 3.2rem); font-weight: 800;
            letter-spacing: -0.5px; margin-bottom: 12px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.2);
            animation: slideDown 0.9s ease 0.2s both;
        }
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        header p {
            font-size: clamp(0.9rem, 2vw, 1.15rem); opacity: 0.95;
            font-weight: 400; max-width: 600px; margin: 0 auto;
            animation: slideDown 0.9s ease 0.4s both;
        }
        .header-tagline {
            display: inline-block; margin-top: 18px; padding: 6px 20px;
            background: rgba(255, 193, 7, 0.95); color: var(--primary-dark);
            border-radius: 30px; font-weight: 600; font-size: 0.85rem;
            letter-spacing: 0.5px;
            animation: slideDown 0.9s ease 0.6s both, shimmer 3s ease-in-out infinite;
        }
        @keyframes shimmer {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        .container { max-width: 1200px; margin: -30px auto 0; padding: 0 20px 60px; position: relative; z-index: 2; }
        .stats-bar {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px; margin-bottom: 35px;
            animation: fadeInUp 0.8s ease 0.5s both;
        }
        .stat-card {
            background: var(--card-bg); border-radius: var(--radius-sm);
            padding: 18px 20px; text-align: center;
            box-shadow: var(--shadow-sm); border: 1px solid var(--border);
            transition: var(--transition);
        }
        .stat-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--primary-light); }
        .stat-value { font-family: 'Poppins', sans-serif; font-size: 1.6rem; font-weight: 700; color: var(--primary); display: block; }
        .stat-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 500; }
        .section-header {
            display: flex; align-items: center; justify-content: space-between;
            flex-wrap: wrap; gap: 15px; margin-bottom: 25px;
            animation: fadeInUp 0.8s ease 0.6s both;
        }
        .section-title {
            font-family: 'Poppins', 'Hind Siliguri', sans-serif;
            font-size: clamp(1.3rem, 3vw, 1.75rem); font-weight: 700;
            color: var(--primary-dark); position: relative; padding-left: 18px;
        }
        .section-title::before {
            content: ''; position: absolute; left: 0; top: 50%;
            transform: translateY(-50%); width: 6px; height: 75%;
            background: linear-gradient(180deg, var(--primary-light), #20c997);
            border-radius: 4px; animation: growBar 0.8s ease 1s both;
        }
        @keyframes growBar { from { height: 0; } to { height: 75%; } }
        .admin-btn {
            display: inline-flex; align-items: center; gap: 8px;
            padding: 10px 22px;
            background: linear-gradient(135deg, var(--primary-dark), var(--primary));
            color: white; border: none; border-radius: 30px;
            font-family: inherit; font-size: 0.9rem; font-weight: 600;
            cursor: pointer; text-decoration: none; transition: var(--transition);
            box-shadow: 0 4px 14px rgba(15, 81, 50, 0.25);
        }
        .admin-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(15, 81, 50, 0.4); }
        .search-filter { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 28px; animation: fadeInUp 0.8s ease 0.7s both; }
        .search-box { position: relative; flex: 1; min-width: 240px; }
        .search-box input {
            width: 100%; padding: 14px 20px 14px 48px;
            border: 2px solid var(--border); border-radius: 40px;
            font-size: 1rem; font-family: inherit; outline: none;
            background: var(--card-bg); transition: var(--transition);
            box-shadow: var(--shadow-sm);
        }
        .search-box input:focus {
            border-color: var(--primary-light);
            box-shadow: 0 0 0 4px rgba(25, 135, 84, 0.12), var(--shadow-md);
            transform: translateY(-2px);
        }
        .search-box::before {
            content: '🔍'; position: absolute; left: 18px; top: 50%;
            transform: translateY(-50%); font-size: 1.05rem; opacity: 0.6; pointer-events: none;
        }
        .filter-chips { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 25px; animation: fadeInUp 0.8s ease 0.8s both; }
        .chip {
            padding: 8px 18px; background: var(--card-bg);
            border: 1.5px solid var(--border); border-radius: 30px;
            font-size: 0.9rem; font-family: inherit; font-weight: 500;
            color: var(--text-muted); cursor: pointer; transition: var(--transition);
            white-space: nowrap;
        }
        .chip:hover { border-color: var(--primary-light); color: var(--primary); transform: translateY(-2px); }
        .chip.active {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white; border-color: transparent;
            box-shadow: 0 4px 14px rgba(25, 135, 84, 0.35);
        }
        .products-grid {
            display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 24px;
        }
        .product-card {
            background: var(--card-bg); border-radius: var(--radius);
            overflow: hidden; box-shadow: var(--shadow-sm);
            border: 1px solid var(--border); transition: var(--transition);
            display: flex; flex-direction: column; position: relative;
            opacity: 0; transform: translateY(30px) scale(0.95);
            animation: cardIn 0.6s ease forwards;
        }
        @keyframes cardIn { to { opacity: 1; transform: translateY(0) scale(1); } }
        .product-card::before {
            content: ''; position: absolute; inset: 0; border-radius: var(--radius); padding: 2px;
            background: linear-gradient(135deg, var(--primary-light), var(--accent), #20c997);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor; mask-composite: exclude;
            opacity: 0; transition: opacity 0.4s ease; pointer-events: none; z-index: 3;
        }
        .product-card:hover::before { opacity: 1; }
        .product-card:hover { transform: translateY(-10px); box-shadow: var(--shadow-lg); }
        .product-image-wrap { position: relative; overflow: hidden; height: 200px; background: linear-gradient(135deg, #f0f4f1, #e2ebe5); }
        .product-image-wrap img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1); }
        .product-card:hover .product-image-wrap img { transform: scale(1.15) rotate(2deg); }
        .product-image-wrap::after {
            content: ''; position: absolute; inset: 0;
            background: linear-gradient(to top, rgba(15, 81, 50, 0.35), transparent 55%);
            opacity: 0; transition: opacity 0.4s ease;
        }
        .product-card:hover .product-image-wrap::after { opacity: 1; }
        .category-badge {
            position: absolute; top: 12px; left: 12px;
            background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
            color: var(--primary-dark); padding: 5px 14px; border-radius: 20px;
            font-size: 0.75rem; font-weight: 600; z-index: 2;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transform: translateX(-120%);
            transition: transform 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        .product-card:hover .category-badge { transform: translateX(0); }
        .product-info {
            padding: 18px 18px 20px; flex-grow: 1;
            display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
        }
        .product-name { font-size: 1.2rem; font-weight: 600; color: var(--text); transition: color 0.3s ease; }
        .product-card:hover .product-name { color: var(--primary); }
        .product-footer { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
        .product-price {
            font-family: 'Poppins', sans-serif; font-size: 1.35rem; font-weight: 700;
            color: var(--primary); display: flex; align-items: baseline; gap: 2px;
        }
        .product-price .currency { font-size: 1rem; font-weight: 600; }
        .product-unit {
            font-size: 0.8rem; color: var(--text-muted); font-weight: 500;
            background: #f0f4f1; padding: 4px 10px; border-radius: 20px;
            transition: var(--transition);
        }
        .product-card:hover .product-unit { background: var(--primary); color: white; }
        .no-result {
            grid-column: 1 / -1; text-align: center;
            padding: 70px 20px; color: var(--text-muted);
            animation: fadeIn 0.5s ease;
        }
        .no-result .emoji { font-size: 4rem; display: block; margin-bottom: 15px; animation: wobble 2s ease infinite; }
        @keyframes wobble {
            0%, 100% { transform: rotate(0); }
            25% { transform: rotate(-10deg); }
            75% { transform: rotate(10deg); }
        }
        footer {
            background: linear-gradient(135deg, var(--primary-dark), var(--primary));
            color: white; padding: 45px 20px 25px; margin-top: 60px;
            position: relative; overflow: hidden;
        }
        footer::before {
            content: ''; position: absolute; top: -50px; left: 0;
            width: 100%; height: 60px; background: var(--bg);
            clip-path: ellipse(75% 100% at 50% 0%);
        }
        .footer-content { max-width: 1200px; margin: 0 auto; text-align: center; position: relative; z-index: 2; }
        .footer-content h3 { font-family: 'Poppins', sans-serif; font-size: 1.4rem; font-weight: 700; margin-bottom: 10px; }
        .footer-content p { opacity: 0.85; font-size: 0.95rem; margin-bottom: 6px; }
        .footer-divider { width: 60px; height: 3px; background: var(--accent); margin: 20px auto; border-radius: 2px; }
        .footer-copy { font-size: 0.85rem; opacity: 0.7; }
        .back-to-top {
            position: fixed; bottom: 30px; right: 30px; width: 50px; height: 50px;
            border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white; border: none; font-size: 1.4rem; cursor: pointer;
            box-shadow: var(--shadow-md); opacity: 0;
            transform: translateY(20px) scale(0.8);
            transition: var(--transition); z-index: 99;
            display: flex; align-items: center; justify-content: center;
        }
        .back-to-top.show { opacity: 1; transform: translateY(0) scale(1); }
        .back-to-top:hover { transform: translateY(-5px) scale(1.1); box-shadow: var(--shadow-glow); }
        .toast {
            position: fixed; bottom: 30px; left: 50%;
            transform: translateX(-50%) translateY(120px);
            background: var(--primary-dark); color: white;
            padding: 12px 24px; border-radius: 30px; font-size: 0.9rem;
            box-shadow: var(--shadow-lg); opacity: 0;
            transition: var(--transition); z-index: 1000;
        }
        .toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
        .toast.error { background: #dc3545; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @media (max-width: 768px) {
            header { padding: 35px 15px 55px; }
            .logo-badge { width: 65px; height: 65px; font-size: 1.7rem; }
            .container { padding: 0 15px 40px; }
            .products-grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; }
            .product-image-wrap { height: 150px; }
            .product-name { font-size: 1rem; }
            .product-price { font-size: 1.1rem; }
            .product-info { padding: 14px; gap: 8px; }
            .back-to-top { bottom: 20px; right: 20px; width: 44px; height: 44px; }
        }
        @media (max-width: 400px) {
            .products-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
            .product-image-wrap { height: 130px; }
            .filter-chips { overflow-x: auto; padding-bottom: 5px; }
            .filter-chips::-webkit-scrollbar { display: none; }
        }
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary-light), var(--primary));
            border-radius: 5px; border: 2px solid var(--bg);
        }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary-dark); }
    </style>
</head>
<body>
    <div class="bg-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>

    <header>
        <div class="header-content">
            <div class="logo-badge">🏪</div>
            <h1>{{ shop_name }}</h1>
            <p>{{ shop_address }}</p>
            <span class="header-tagline">✨ বিশ্বস্ত ও সাশ্রয়ী দামে ✨</span>
        </div>
    </header>

    <div class="container">
        <div class="stats-bar">
            <div class="stat-card">
                <span class="stat-value" id="totalProducts">{{ products|length }}+</span>
                <span class="stat-label">মোট পণ্য</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">১০০%</span>
                <span class="stat-label">খাঁটি পণ্য</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">২৪/৭</span>
                <span class="stat-label">সেবা</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">✓</span>
                <span class="stat-label">সাশ্রয়ী দাম</span>
            </div>
        </div>

        <div class="section-header">
            <h2 class="section-title">আমাদের পণ্যসমূহ</h2>
            <a href="/admin" class="admin-btn">🔐 অ্যাডমিন প্যানেল</a>
        </div>

        <div class="search-filter">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="পণ্য খুঁজুন... (যেমন: চাল, ডাল)" autocomplete="off">
            </div>
        </div>

        <div class="filter-chips" id="filterChips">
            <button class="chip active" data-category="all">সব পণ্য</button>
            {% for cat in categories %}
            <button class="chip" data-category="{{ cat }}">{{ cat }}</button>
            {% endfor %}
        </div>

        <div class="products-grid" id="productsGrid">
            {% for product in products %}
            <div class="product-card" data-name="{{ product.name }}" data-category="{{ product.category }}" style="animation-delay: {{ loop.index0 * 0.05 }}s">
                <div class="product-image-wrap">
                    <span class="category-badge">{{ product.category }}</span>
                    <img src="{{ product.image }}" alt="{{ product.name }}" loading="lazy"
                         onerror="this.src='https://via.placeholder.com/400x400/198754/ffffff?text={{ product.name }}'">
                </div>
                <div class="product-info">
                    <div class="product-name">{{ product.name }}</div>
                    <div class="product-footer">
                        <div class="product-price"><span class="currency">৳</span>{{ product.price }}</div>
                        <div class="product-unit">/ {{ product.unit }}</div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <button class="back-to-top" id="backToTop">↑</button>
    <div class="toast" id="toast"></div>

    <footer>
        <div class="footer-content">
            <h3>🏪 {{ shop_name }}</h3>
            <p>{{ shop_address }}</p>
            <div class="footer-divider"></div>
            <p class="footer-copy">© ২০২৬ {{ shop_name }}। সর্বস্বত্ব সংরক্ষিত।</p>
        </div>
    </footer>

    <script>
        const searchInput = document.getElementById('searchInput');
        const productsGrid = document.getElementById('productsGrid');
        const filterChips = document.getElementById('filterChips');
        const backToTop = document.getElementById('backToTop');
        const toast = document.getElementById('toast');
        let allCards = [...document.querySelectorAll('.product-card')];
        let activeCategory = 'all';
        let activeSearch = '';

        function showToast(message, isError = false) {
            toast.textContent = message;
            toast.classList.toggle('error', isError);
            toast.classList.add('show');
            clearTimeout(toast._timer);
            toast._timer = setTimeout(() => toast.classList.remove('show'), 2200);
        }

        function filterProducts() {
            let visibleCount = 0;
            allCards.forEach(card => {
                const name = card.dataset.name.toLowerCase();
                const category = card.dataset.category;
                const matchSearch = name.includes(activeSearch);
                const matchCategory = activeCategory === 'all' || category === activeCategory;
                if (matchSearch && matchCategory) {
                    card.style.display = 'flex';
                    card.style.animation = 'none';
                    void card.offsetWidth;
                    card.style.animation = 'cardIn 0.5s ease forwards';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });
            const oldMsg = productsGrid.querySelector('.no-result');
            if (oldMsg) oldMsg.remove();
            if (visibleCount === 0) {
                const msg = document.createElement('div');
                msg.className = 'no-result';
                msg.innerHTML = '<span class="emoji">🔍</span><p>কোনো পণ্য পাওয়া যায়নি</p>';
                productsGrid.appendChild(msg);
            }
        }

        let searchTimer;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(() => {
                activeSearch = e.target.value.trim().toLowerCase();
                filterProducts();
            }, 200);
        });

        filterChips.addEventListener('click', (e) => {
            const chip = e.target.closest('.chip');
            if (!chip) return;
            filterChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            activeCategory = chip.dataset.category;
            filterProducts();
            showToast(`"${chip.textContent.trim()}" বিভাগ দেখানো হচ্ছে`);
        });

        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) backToTop.classList.add('show');
            else backToTop.classList.remove('show');
        });
        backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

        allCards.forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                const rotateX = ((y - rect.height / 2) / (rect.height / 2)) * -4;
                const rotateY = ((x - rect.width / 2) / (rect.width / 2)) * 4;
                card.style.transform = `translateY(-10px) perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });
            card.addEventListener('mouseleave', () => card.style.transform = '');
        });

        window.addEventListener('load', () => {
            setTimeout(() => showToast('🏪 {{ shop_name }}-এ স্বাগতম!'), 800);
        });

        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchInput.focus();
                showToast('অনুসন্ধান বক্সে ফোকাস করা হয়েছে');
            }
        });
    </script>
</body>
</html>
"""

# ==================== Login Template ====================
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>অ্যাডমিন লগইন — {{ shop_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Hind Siliguri', 'Poppins', sans-serif;
            min-height: 100vh; display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, #0a3622 0%, #0f5132 50%, #198754 100%);
            background-size: 200% 200%; animation: gradientShift 12s ease infinite;
            padding: 20px; position: relative; overflow: hidden;
        }
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        body::before {
            content: ''; position: absolute; width: 500px; height: 500px;
            border-radius: 50%; background: rgba(255, 193, 7, 0.15);
            filter: blur(100px); top: -150px; left: -150px;
            animation: floatShape 15s ease-in-out infinite;
        }
        body::after {
            content: ''; position: absolute; width: 400px; height: 400px;
            border-radius: 50%; background: rgba(32, 201, 151, 0.2);
            filter: blur(100px); bottom: -120px; right: -120px;
            animation: floatShape 18s ease-in-out infinite reverse;
        }
        @keyframes floatShape {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(60px, -40px); }
        }
        .login-card {
            background: rgba(255, 255, 255, 0.98); backdrop-filter: blur(20px);
            border-radius: 24px; padding: 45px 35px;
            max-width: 420px; width: 100%;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
            position: relative; z-index: 2;
            animation: cardIn 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        @keyframes cardIn {
            from { opacity: 0; transform: translateY(40px) scale(0.9); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .login-icon {
            width: 80px; height: 80px; border-radius: 50%;
            background: linear-gradient(135deg, #0f5132, #198754);
            display: flex; align-items: center; justify-content: center;
            margin: 0 auto 20px; font-size: 2.2rem; color: white;
            box-shadow: 0 10px 30px rgba(15, 81, 50, 0.35);
            animation: pulseGlow 3s ease-in-out infinite;
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 10px 30px rgba(15, 81, 50, 0.35); }
            50% { box-shadow: 0 10px 40px rgba(15, 81, 50, 0.6); }
        }
        .login-card h1 {
            font-family: 'Poppins', sans-serif; text-align: center;
            font-size: 1.6rem; font-weight: 700; color: #0a3622; margin-bottom: 8px;
        }
        .login-card p { text-align: center; color: #6c757d; font-size: 0.9rem; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; font-size: 0.85rem; font-weight: 600; color: #0a3622; margin-bottom: 8px; }
        .form-group input {
            width: 100%; padding: 14px 18px; border: 2px solid #e0e6e2;
            border-radius: 12px; font-size: 1rem; font-family: inherit;
            outline: none; transition: all 0.3s ease; background: #f9fbfa;
        }
        .form-group input:focus {
            border-color: #198754; background: white;
            box-shadow: 0 0 0 4px rgba(25, 135, 84, 0.12);
        }
        .btn-login {
            width: 100%; padding: 14px;
            background: linear-gradient(135deg, #0f5132, #198754);
            color: white; border: none; border-radius: 12px;
            font-size: 1rem; font-family: inherit; font-weight: 600;
            cursor: pointer; transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(15, 81, 50, 0.3); margin-top: 8px;
        }
        .btn-login:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(15, 81, 50, 0.45); }
        .error-msg {
            background: #f8d7da; color: #dc3545;
            padding: 12px 16px; border-radius: 10px; font-size: 0.9rem;
            margin-bottom: 18px; border-left: 4px solid #dc3545;
            animation: shake 0.5s ease;
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-8px); }
            75% { transform: translateX(8px); }
        }
        .back-link {
            display: block; text-align: center; margin-top: 20px;
            color: #6c757d; text-decoration: none; font-size: 0.9rem;
            transition: color 0.3s ease;
        }
        .back-link:hover { color: #0f5132; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="login-icon">🔐</div>
        <h1>অ্যাডমিন লগইন</h1>
        <p>{{ shop_name }} — নিয়ন্ত্রণ কেন্দ্র</p>
        {% if error %}
        <div class="error-msg">⚠️ {{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="form-group">
                <label>🔑 পাসওয়ার্ড</label>
                <input type="password" name="password" placeholder="পাসওয়ার্ড লিখুন" required autofocus>
            </div>
            <button type="submit" class="btn-login">লগইন করুন →</button>
        </form>
        <a href="/" class="back-link">← দোকানে ফিরে যান</a>
    </div>
</body>
</html>
"""

# ==================== Admin Panel Template ====================
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>অ্যাডমিন প্যানেল — {{ shop_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --primary: #0f5132; --primary-light: #198754; --primary-dark: #0a3622;
            --accent: #ffc107; --danger: #dc3545; --success: #198754;
            --bg: #f4f7f5; --card-bg: #ffffff;
            --text: #1a1a1a; --text-muted: #6c757d; --border: #e0e6e2;
            --shadow-sm: 0 2px 8px rgba(15, 81, 50, 0.06);
            --shadow-md: 0 8px 24px rgba(15, 81, 50, 0.10);
            --shadow-lg: 0 16px 48px rgba(15, 81, 50, 0.18);
            --radius: 16px;
            --transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }
        body {
            font-family: 'Hind Siliguri', 'Poppins', sans-serif;
            background: var(--bg); color: var(--text);
            line-height: 1.6; min-height: 100vh; padding-bottom: 40px;
        }
        .topbar {
            background: linear-gradient(135deg, var(--primary-dark), var(--primary));
            color: white; padding: 18px 24px;
            display: flex; align-items: center; justify-content: space-between;
            flex-wrap: wrap; gap: 12px;
            box-shadow: var(--shadow-md); position: sticky; top: 0; z-index: 50;
        }
        .topbar-brand { display: flex; align-items: center; gap: 12px; font-family: 'Poppins', sans-serif; font-size: 1.15rem; font-weight: 700; }
        .topbar-brand .badge-icon {
            width: 40px; height: 40px; border-radius: 10px;
            background: rgba(255,255,255,0.15);
            display: flex; align-items: center; justify-content: center; font-size: 1.3rem;
        }
        .topbar-actions { display: flex; gap: 10px; flex-wrap: wrap; }
        .topbar-actions a, .topbar-actions button {
            padding: 9px 18px; border-radius: 30px;
            border: 1.5px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.1); color: white;
            text-decoration: none; font-family: inherit;
            font-size: 0.85rem; font-weight: 600;
            cursor: pointer; transition: var(--transition);
            display: inline-flex; align-items: center; gap: 6px;
        }
        .topbar-actions a:hover, .topbar-actions button:hover {
            background: rgba(255,255,255,0.25); transform: translateY(-2px);
        }
        .topbar-actions .logout-btn { background: rgba(220, 53, 69, 0.8); border-color: rgba(220, 53, 69, 0.8); }
        .topbar-actions .logout-btn:hover { background: var(--danger); }
        .container { max-width: 1200px; margin: 0 auto; padding: 30px 20px; }
        .page-title {
            font-family: 'Poppins', sans-serif; font-size: 1.7rem;
            font-weight: 700; color: var(--primary-dark); margin-bottom: 8px;
            animation: fadeInUp 0.5s ease both;
        }
        .page-subtitle { color: var(--text-muted); margin-bottom: 25px; animation: fadeInUp 0.5s ease 0.1s both; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .admin-stats {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px; margin-bottom: 30px;
            animation: fadeInUp 0.5s ease 0.2s both;
        }
        .admin-stat {
            background: var(--card-bg); border-radius: var(--radius);
            padding: 22px; box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
            transition: var(--transition); position: relative; overflow: hidden;
        }
        .admin-stat::before {
            content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%;
            background: linear-gradient(180deg, var(--primary-light), #20c997);
        }
        .admin-stat:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
        .admin-stat .value { font-family: 'Poppins', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary); display: block; }
        .admin-stat .label { font-size: 0.9rem; color: var(--text-muted); font-weight: 500; }
        .add-section {
            background: var(--card-bg); border-radius: var(--radius);
            padding: 28px; box-shadow: var(--shadow-sm);
            border: 1px solid var(--border); margin-bottom: 30px;
            animation: fadeInUp 0.5s ease 0.3s both;
        }
        .section-head {
            display: flex; align-items: center; gap: 10px;
            margin-bottom: 20px; padding-bottom: 15px;
            border-bottom: 2px solid var(--border);
        }
        .section-head .icon {
            width: 42px; height: 42px; border-radius: 12px;
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white; display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem; box-shadow: 0 4px 12px rgba(15, 81, 50, 0.25);
        }
        .section-head h2 { font-family: 'Poppins', sans-serif; font-size: 1.2rem; font-weight: 700; color: var(--primary-dark); }
        .form-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px; margin-bottom: 20px;
        }
        .form-field label { display: block; font-size: 0.85rem; font-weight: 600; color: var(--primary-dark); margin-bottom: 6px; }
        .form-field input, .form-field select {
            width: 100%; padding: 11px 14px;
            border: 2px solid var(--border); border-radius: 10px;
            font-size: 0.95rem; font-family: inherit; outline: none;
            transition: var(--transition); background: #f9fbfa;
        }
        .form-field input:focus, .form-field select:focus {
            border-color: var(--primary-light); background: white;
            box-shadow: 0 0 0 4px rgba(25, 135, 84, 0.12);
        }
        .btn {
            padding: 12px 24px; border: none; border-radius: 10px;
            font-family: inherit; font-size: 0.95rem; font-weight: 600;
            cursor: pointer; transition: var(--transition);
            display: inline-flex; align-items: center; gap: 8px;
        }
        .btn-add {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white; box-shadow: 0 6px 20px rgba(15, 81, 50, 0.25);
        }
        .btn-add:hover { transform: translateY(-3px); box-shadow: 0 10px 28px rgba(15, 81, 50, 0.4); }
        .list-section {
            background: var(--card-bg); border-radius: var(--radius);
            padding: 28px; box-shadow: var(--shadow-sm);
            border: 1px solid var(--border);
            animation: fadeInUp 0.5s ease 0.4s both;
        }
        .product-list { display: grid; gap: 12px; }
        .product-row {
            display: grid; grid-template-columns: 70px 1fr auto auto;
            gap: 16px; align-items: center;
            padding: 14px 16px; background: #f9fbfa;
            border-radius: 12px; border: 1px solid var(--border);
            transition: var(--transition); animation: rowIn 0.4s ease both;
        }
        @keyframes rowIn { from { opacity: 0; transform: translateX(-20px); } to { opacity: 1; transform: translateX(0); } }
        .product-row:hover {
            background: white; box-shadow: var(--shadow-md);
            border-color: var(--primary-light); transform: translateX(4px);
        }
        .product-row img { width: 60px; height: 60px; border-radius: 10px; object-fit: cover; background: #eaeaea; }
        .product-row .info h4 { font-size: 1.05rem; font-weight: 600; color: var(--text); margin-bottom: 4px; }
        .product-row .info .meta { display: flex; gap: 12px; flex-wrap: wrap; font-size: 0.85rem; color: var(--text-muted); }
        .product-row .info .meta .price { color: var(--primary); font-weight: 700; font-family: 'Poppins', sans-serif; }
        .product-row .info .meta .tag {
            background: #e8f5ee; color: var(--primary-dark);
            padding: 2px 10px; border-radius: 20px;
            font-weight: 600; font-size: 0.75rem;
        }
        .btn-delete {
            background: rgba(220, 53, 69, 0.1); color: var(--danger);
            border: 1.5px solid rgba(220, 53, 69, 0.3);
            padding: 9px 16px; border-radius: 10px;
            font-size: 0.85rem; font-weight: 600;
            cursor: pointer; font-family: inherit;
            transition: var(--transition);
            display: inline-flex; align-items: center; gap: 6px;
        }
        .btn-delete:hover {
            background: var(--danger); color: white;
            border-color: var(--danger); transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(220, 53, 69, 0.35);
        }
        .empty-state { text-align: center; padding: 60px 20px; color: var(--text-muted); }
        .empty-state .emoji { font-size: 3.5rem; display: block; margin-bottom: 12px; }
        .alert {
            padding: 14px 20px; border-radius: 12px;
            margin-bottom: 20px; font-weight: 500;
            display: flex; align-items: center; gap: 10px;
            animation: slideDown 0.4s ease;
        }
        @keyframes slideDown { from { opacity: 0; transform: translateY(-15px); } to { opacity: 1; transform: translateY(0); } }
        .alert-success { background: #d1e7dd; color: #0f5132; border-left: 4px solid var(--success); }
        .alert-error { background: #f8d7da; color: #842029; border-left: 4px solid var(--danger); }
        @media (max-width: 768px) {
            .product-row { grid-template-columns: 60px 1fr; gap: 12px; }
            .product-row .btn-delete { grid-column: 2; justify-self: start; }
            .topbar-brand { font-size: 1rem; }
            .page-title { font-size: 1.3rem; }
        }
    </style>
</head>
<body>
    <div class="topbar">
        <div class="topbar-brand">
            <span class="badge-icon">🔐</span>
            <span>অ্যাডমিন প্যানেল — {{ shop_name }}</span>
        </div>
        <div class="topbar-actions">
            <a href="/">🏪 দোকান দেখুন</a>
            <a href="/logout" class="logout-btn">🚪 লগআউট</a>
        </div>
    </div>

    <div class="container">
        {% if message %}
        <div class="alert alert-success">✅ {{ message }}</div>
        {% endif %}
        {% if error %}
        <div class="alert alert-error">⚠️ {{ error }}</div>
        {% endif %}

        <h1 class="page-title">📊 ড্যাশবোর্ড</h1>
        <p class="page-subtitle">পণ্য যোগ করুন, মুছে ফেলুন — সব পরিবর্তন সাথে সাথে লাইভ হবে</p>

        <div class="admin-stats">
            <div class="admin-stat">
                <span class="value">{{ products|length }}</span>
                <span class="label">মোট পণ্য</span>
            </div>
            <div class="admin-stat">
                <span class="value">{{ categories|length }}</span>
                <span class="label">ক্যাটাগরি</span>
            </div>
            <div class="admin-stat">
                <span class="value">২৪/৭</span>
                <span class="label">লাইভ স্ট্যাটাস</span>
            </div>
        </div>

        <div class="add-section">
            <div class="section-head">
                <div class="icon">➕</div>
                <h2>নতুন পণ্য যোগ করুন</h2>
            </div>
            <form method="POST" action="/admin/add">
                <div class="form-grid">
                    <div class="form-field">
                        <label>পণ্যের নাম *</label>
                        <input type="text" name="name" placeholder="যেমন: চাল" required>
                    </div>
                    <div class="form-field">
                        <label>দাম (৳) *</label>
                        <input type="number" name="price" placeholder="যেমন: 70" step="0.01" min="0" required>
                    </div>
                    <div class="form-field">
                        <label>একক *</label>
                        <select name="unit" required>
                            <option value="কেজি">কেজি</option>
                            <option value="গ্রাম">গ্রাম</option>
                            <option value="লিটার">লিটার</option>
                            <option value="মিলিলিটার">মিলিলিটার</option>
                            <option value="পিস">পিস</option>
                            <option value="প্যাকেট">প্যাকেট</option>
                            <option value="বোতল">বোতল</option>
                            <option value="ডজন">ডজন</option>
                        </select>
                    </div>
                    <div class="form-field">
                        <label>ক্যাটাগরি *</label>
                        <select name="category" required>
                            <option value="মুদি">মুদি</option>
                            <option value="স্ন্যাকস">স্ন্যাকস</option>
                            <option value="পানীয়">পানীয়</option>
                            <option value="মিষ্টি">মিষ্টি</option>
                            <option value="প্রসাধনী">প্রসাধনী</option>
                            <option value="অন্যান্য">অন্যান্য</option>
                        </select>
                    </div>
                </div>
                <div class="form-field" style="margin-bottom: 20px;">
                    <label>ছবির URL (ঐচ্ছিক)</label>
                    <input type="url" name="image" placeholder="https://example.com/image.jpg — খালি রাখলে ডিফল্ট ছবি ব্যবহার হবে">
                </div>
                <button type="submit" class="btn btn-add">➕ পণ্য যোগ করুন</button>
            </form>
        </div>

        <div class="list-section">
            <div class="section-head">
                <div class="icon">📦</div>
                <h2>সকল পণ্য ({{ products|length }})</h2>
            </div>

            {% if products %}
            <div class="product-list">
                {% for product in products %}
                <div class="product-row" style="animation-delay: {{ loop.index0 * 0.03 }}s">
                    <img src="{{ product.image }}" alt="{{ product.name }}"
                         onerror="this.src='https://via.placeholder.com/100x100/198754/ffffff?text={{ product.name }}'">
                    <div class="info">
                        <h4>{{ product.name }}</h4>
                        <div class="meta">
                            <span class="price">৳ {{ product.price }} / {{ product.unit }}</span>
                            <span class="tag">{{ product.category }}</span>
                        </div>
                    </div>
                    <form method="POST" action="/admin/delete/{{ product.id }}" style="display:inline;"
                          onsubmit="return confirm('আপনি কি নিশ্চিত মুছে ফেলতে চান?');">
                        <button type="submit" class="btn-delete">🗑️ মুছুন</button>
                    </form>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="empty-state">
                <span class="emoji">📭</span>
                <p>এখনো কোনো পণ্য যোগ করা হয়নি</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# ==================== Routes ====================
@app.route('/')
def home():
    products = load_products()
    categories = get_categories(products)
    return render_template_string(
        HTML_TEMPLATE,
        shop_name=SHOP_NAME,
        shop_address=SHOP_ADDRESS,
        products=products,
        categories=categories
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if is_logged_in():
        return redirect(url_for('admin_panel'))
    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = "ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।"
    return render_template_string(LOGIN_TEMPLATE, shop_name=SHOP_NAME, error=error)

@app.route('/admin/panel')
def admin_panel():
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    products = load_products()
    categories = get_categories(products)
    message = request.args.get('message')
    error = request.args.get('error')
    return render_template_string(
        ADMIN_TEMPLATE,
        shop_name=SHOP_NAME,
        products=products,
        categories=categories,
        message=message,
        error=error
    )

@app.route('/admin/add', methods=['POST'])
def admin_add():
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    try:
        name = request.form.get('name', '').strip()
        price = float(request.form.get('price', 0))
        unit = request.form.get('unit', '').strip()
        category = request.form.get('category', '').strip()
        image = request.form.get('image', '').strip()
        if not name or price <= 0 or not unit or not category:
            return redirect(url_for('admin_panel', error="সব ঘর পূরণ করুন"))
        if not image:
            image = f"https://via.placeholder.com/400x400/198754/ffffff?text={name}"
        products = load_products()
        new_id = max([p['id'] for p in products], default=0) + 1
        products.append({
            "id": new_id, "name": name, "price": price,
            "unit": unit, "category": category, "image": image
        })
        save_products(products)
        return redirect(url_for('admin_panel', message=f"'{name}' সফলভাবে যোগ হয়েছে"))
    except Exception as e:
        return redirect(url_for('admin_panel', error=f"সমস্যা: {str(e)}"))

@app.route('/admin/delete/<int:product_id>', methods=['POST'])
def admin_delete(product_id):
    if not is_logged_in():
        return redirect(url_for('admin_login'))
    products = load_products()
    product_name = next((p['name'] for p in products if p['id'] == product_id), "পণ্য")
    products = [p for p in products if p['id'] != product_id]
    save_products(products)
    return redirect(url_for('admin_panel', message=f"'{product_name}' সফলভাবে মুছে ফেলা হয়েছে"))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/api/products')
def api_products():
    return jsonify(load_products())

# ==================== Run ====================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
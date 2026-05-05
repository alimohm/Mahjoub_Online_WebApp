<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}القيادة المركزية | محجوب أونلاين{% endblock %}</title>
    
    <!-- الخطوط والأيقونات السيادية -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    
    <style>
        :root {
            --royal-purple: #1a0b2e;
            --deep-black: #08020d;
            --mahjoub-gold: #D4AF37;
            --sidebar-width: 280px;
            --sidebar-mini: 85px;
            --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            --polished-stone: #e0e0e0; 
        }

        body { 
            font-family: 'Cairo', sans-serif; 
            background: #f8f9fa; 
            margin: 0; display: flex; direction: rtl; min-height: 100vh;
            overflow-x: hidden;
        }

        /* أنيميشن الشعار */
        @keyframes logo-pulse {
            0% { filter: brightness(0) invert(1) drop-shadow(0 0 10px rgba(212, 175, 55, 0.3)); transform: scale(1); }
            50% { filter: brightness(0) invert(1) drop-shadow(0 0 20px rgba(212, 175, 55, 0.6)); transform: scale(1.05); }
            100% { filter: brightness(0) invert(1) drop-shadow(0 0 10px rgba(212, 175, 55, 0.3)); transform: scale(1); }
        }

        .sidebar {
            width: var(--sidebar-width);
            background: linear-gradient(180deg, var(--royal-purple) 0%, var(--deep-black) 100%);
            height: 100vh; position: fixed; right: 0; top: 0;
            z-index: 1100; display: flex; flex-direction: column;
            transition: var(--transition);
            box-shadow: -5px 0 25px rgba(0,0,0,0.5);
        }

        .sidebar-header { 
            padding: 2.5rem 1rem; text-align: center; 
            border-bottom: 1px solid rgba(212, 175, 55, 0.15);
        }
        
        .logo-img { 
            width: 75px; height: auto; 
            margin-bottom: 15px; 
            animation: logo-pulse 4s infinite ease-in-out;
        }
        
        .sidebar-header h2 { color: white; font-size: 1.25rem; margin: 0; font-weight: 900; }
        .platform-desc { color: var(--mahjoub-gold); font-size: 0.7rem; font-weight: 800; margin-top: 5px; }

        .nav-menu { padding: 1.2rem 1rem; flex-grow: 1; overflow-y: auto; }
        
        .nav-link {
            display: flex; align-items: center; padding: 14px 18px;
            color: rgba(255, 255, 255, 0.65); text-decoration: none;
            border-radius: 15px; margin-bottom: 5px; transition: var(--transition);
            font-weight: 600;
        }

        .nav-link i { min-width: 35px; font-size: 1.3rem; }
        
        .nav-link:hover, .nav-link.active {
            background: rgba(212, 175, 55, 0.12); color: var(--mahjoub-gold);
            transform: translateX(-10px);
        }

        .dropdown-content {
            display: none; list-style: none; padding: 5px 0; margin-right: 2.5rem;
            border-right: 2px solid rgba(212, 175, 55, 0.2);
            animation: slideIn 0.3s ease-out;
        }

        .main-wrapper { 
            margin-right: var(--sidebar-width); width: calc(100% - var(--sidebar-width)); 
            transition: var(--transition);
        }

        .top-bar {
            background: rgba(255, 255, 255, 0.95); height: 85px; 
            display: flex; align-items: center; justify-content: space-between; padding: 0 3rem;
            box-shadow: 0 2px 15px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 1000;
        }

        .user-avatar { 
            width: 48px; height: 48px; background: var(--royal-purple); 
            border-radius: 12px; display: flex; align-items: center; 
            justify-content: center; color: var(--mahjoub-gold);
            border: 1px solid var(--mahjoub-gold);
        }

        .content-area { padding: 3rem; min-height: calc(100vh - 85px); }

        @media (max-width: 992px) {
            .sidebar { width: var(--sidebar-mini); }
            .sidebar-header h2, .platform-desc, .nav-link span, .dropdown-content { display: none !important; }
            .main-wrapper { margin-right: var(--sidebar-mini); width: calc(100% - var(--sidebar-mini)); }
        }
    </style>
</head>
<body>

    <aside class="sidebar">
        <div class="sidebar-header">
            <img src="https://cdn.qumra.cloud/media/67f7f6d5f0b82f44a47bf845/1770229315912-117966978.webp" class="logo-img" alt="Logo">
            <h2>محجوب أونلاين</h2>
            <div class="platform-desc">نظام الإدارة المركزي</div>
        </div>

        <nav class="nav-menu">
            <!-- الربط الصحيح بدالة admin_dashboard -->
            <a href="{{ url_for('admin.admin_dashboard') }}" class="nav-link {% if request.endpoint == 'admin.admin_dashboard' %}active{% endif %}">
                <i class="fas fa-tower-observation"></i>
                <span>مركز القيادة</span>
            </a>

            <!-- الربط الصحيح بدالة manage_suppliers -->
            <a href="{{ url_for('admin.manage_suppliers') }}" class="nav-link {% if request.endpoint == 'admin.manage_suppliers' %}active{% endif %}">
                <i class="fas fa-handshake-angle"></i>
                <span>إدارة الموردين</span>
            </a>

            <div class="nav-item">
                <div class="nav-link" onclick="toggleDropdown(this)">
                    <i class="fas fa-vault"></i>
                    <span>الهندسة المالية</span>
                    <i class="fas fa-chevron-down ms-auto" style="font-size: 0.7rem;"></i>
                </div>
                <ul class="dropdown-content">
                    <li><a href="#" class="nav-link">المحافظ السيادية</a></li>
                    <li><a href="#" class="nav-link">طلبات الصرف</a></li>
                </ul>
            </div>

            <!-- الربط الصحيح بدالة logout -->
            <a href="{{ url_for('admin.logout') }}" class="nav-link mt-auto" style="color: #ff7675;">
                <i class="fas fa-sign-out-alt"></i>
                <span>إنهاء الجلسة</span>
            </a>
        </nav>
    </aside>

    <main class="main-wrapper">
        <header class="top-bar">
            <div class="user-profile d-flex align-items-center gap-3">
                <div class="user-avatar">
                    <i class="fas fa-crown"></i>
                </div>
                <div>
                    <div style="font-weight: 900; color: var(--royal-purple);">
                        {{ current_user.username if current_user.is_authenticated else 'علي محجوب' }}
                    </div>
                    <div style="color: #6c757d; font-size: 0.75rem;">المؤسس والمدير الأعلى</div>
                </div>
            </div>
        </header>

        <div class="content-area">
            {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                {% for category, message in messages %}
                  <div class="alert alert-info alert-dismissible fade show mb-4" role="alert">
                      {{ message }}
                      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                  </div>
                {% endfor %}
              {% endif %}
            {% endwith %}

            {% block content %}{% endblock %}
        </div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleDropdown(element) {
            const content = element.nextElementSibling;
            content.style.display = content.style.display === "block" ? "none" : "block";
        }
    </script>
</body>
</html>

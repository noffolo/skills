// ==UserScript==
// @name         WebChat Enhancer
// @namespace    https://clawhub.ai/skills/webchat-enhancer
// @version      4.5.0
// @description  🌟 Enhance OpenClaw WebChat
// @author       Boss
// @match        http://127.0.0.1:18789/*
// @match        http://localhost:18789/*
// @grant        GM_addStyle
// @run-at       document-idle
// @license      MIT
// ==/UserScript==

(function() {
    "use strict";

    var LANG = {
        title: "Navigator",
        generating: "Loading...",
        noMessages: "No messages",
        latest: "Latest",
        msgs: "msgs"
    };

    var THEMES = {
        dark: {
            bg: "rgba(20, 20, 25, 0.96)",
            card: "rgba(30, 28, 38, 0.98)",
            border: "rgba(192, 57, 43, 0.18)",
            text: "#e8e4e0",
            muted: "#7a746e",
            accent: "#c0392b",
            success: "#27ae60",
            tabBg: "rgba(20, 20, 25, 0.96)",
            tabBorder: "rgba(192, 57, 43, 0.25)",
            tabIcon: "#c0392b",
            tabText: "#c0392b"
        },
        light: {
            bg: "rgba(247, 247, 247, 0.95)",
            card: "#ffffff",
            border: "rgba(192, 57, 43, 0.2)",
            text: "#2c2c2c",
            muted: "#9a948e",
            accent: "#c0392b",
            success: "#27ae60",
            tabBg: "rgba(247, 247, 247, 0.95)",
            tabBorder: "rgba(192, 57, 43, 0.25)",
            tabIcon: "#c0392b",
            tabText: "#c0392b"
        }
    };

    var PANEL_W = 300;
    var TAB_W = 36;

    var currentThemeName = "dark";
    var theme = THEMES.dark;

    function buildCss(t) {
        return [
            ".wce-wrap{position:fixed;top:120px;right:0;z-index:9999;display:flex;align-items:flex-start;}",
            ".wce-buffer{flex-shrink:0;width:1px;height:100%;min-height:200px}",
            ".wce-panel{transform:translateX(" + (PANEL_W + TAB_W + 1) + "px);transition:transform 0.3s cubic-bezier(0.4,0,0.2,1);will-change:transform;}",
            ".wce-wrap.open .wce-panel{transform:translateX(0)}",
            ".wce-wrap.open .wce-tab{opacity:0;pointer-events:none;width:0;overflow:hidden;border-width:0;padding:0;margin:0}",
            ".wce-tab{width:" + TAB_W + "px;background:" + t.tabBg + ";backdrop-filter:blur(24px);border:1px solid " + t.tabBorder + ";border-right:none;border-radius:12px 0 0 12px;padding:16px 6px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:10px;opacity:0.85;transition:opacity 0.2s, width 0.3s, padding 0.3s, border-width 0.3s, margin 0.3s;flex-shrink:0;}",
            ".wce-tab:hover{opacity:1}",
            ".wce-tab-icon{width:18px;height:18px;border-left:2px solid " + t.tabIcon + ";border-bottom:2px solid " + t.tabIcon + ";transform:rotate(-45deg);flex-shrink:0}",
            ".wce-tab-text{writing-mode:vertical-rl;text-orientation:mixed;font-size:11px;font-weight:600;color:" + t.tabText + ";letter-spacing:1px}",
            ".wce-panel-inner{width:" + PANEL_W + "px;background:" + t.bg + ";backdrop-filter:blur(24px);border:1px solid " + t.border + ";border-radius:20px 0 0 20px;z-index:9999;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;overflow:hidden;box-shadow:0 25px 80px rgba(0,0,0,0.15);max-height:70vh;display:flex;flex-direction:column}",
            ".wce-header{padding:16px 18px;background:" + t.card + ";border-bottom:1px solid " + t.border + ";user-select:none}",
            ".wce-header h3{font-size:13px;font-weight:600;color:" + t.text + ";margin:0;letter-spacing:-0.02em}",
            ".wce-body{flex:1;padding:10px;max-height:calc(70vh - 100px);overflow-y:auto}",
            ".wce-body::-webkit-scrollbar{width:5px}",
            ".wce-body::-webkit-scrollbar-track{background:transparent}",
            ".wce-body::-webkit-scrollbar-thumb{background:" + t.border + ";border-radius:3px}",
            ".wce-item{display:flex;align-items:center;gap:10px;background:" + t.card + ";border:1px solid " + t.border + ";border-radius:10px;padding:10px 12px;margin-bottom:6px;cursor:pointer;transition:all 0.15s}",
            ".wce-item:hover{background:" + t.accent + "15;border-color:" + t.accent + "40}",
            ".wce-item:active{transform:scale(0.97)}",
            ".wce-item.latest{border-color:" + t.success + "50;background:" + t.success + "10}",
            ".wce-item.clicked{animation:wce-pulse 0.4s ease}",
            "@keyframes wce-pulse{0%{transform:scale(1)}50%{transform:scale(0.95);background:" + t.accent + "25}100%{transform:scale(1)}}",
            ".wce-num{font-size:11px;font-weight:700;color:" + t.accent + ";min-width:20px}",
            ".wce-item.latest .wce-num{color:" + t.success + "}",
            ".wce-preview{font-size:12px;color:" + t.text + ";line-height:1.4;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
            ".wce-badge{font-size:9px;font-weight:600;color:" + t.success + ";background:" + t.success + "20;padding:2px 6px;border-radius:5px}",
            ".wce-empty{text-align:center;padding:40px 16px;color:" + t.muted + ";font-size:12px}",
            ".wce-footer{display:flex;gap:6px;padding:10px 14px;border-top:1px solid " + t.border + ";background:" + t.card + "}",
            ".wce-btn{flex:1;padding:8px;border:1px solid " + t.border + ";border-radius:8px;font-size:11px;font-weight:500;cursor:pointer;background:" + t.accent + ";color:#fff;border:none;transition:all 0.15s;text-align:center}",
            ".wce-btn:hover{filter:brightness(1.1)}",
            ".wce-count{font-size:11px;color:" + t.muted + ";margin-left:auto}",
            ".wce-count span{color:" + t.accent + ";font-weight:600}",
            ".wce-toast{position:fixed;bottom:200px;left:50%;transform:translateX(-50%) translateY(20px);background:" + t.card + ";color:" + t.text + ";padding:8px 20px;border-radius:16px;font-size:12px;box-shadow:0 10px 40px rgba(0,0,0,0.15);z-index:10002;opacity:0;transition:all 0.3s;pointer-events:none}",
            ".wce-toast.show{opacity:1;transform:translateX(-50%) translateY(0)}"
        ].join("");
    }

    var styleEl = document.createElement("style");
    styleEl.id = "wce-dynamic-css";
    document.head.appendChild(styleEl);

    function applyTheme(t) {
        theme = t;
        styleEl.textContent = buildCss(t);
    }

    function detectTheme() {
        var newTheme = "dark";
        var body = document.body;
        var className = body.className + " " + (body.getAttribute("data-theme") || "") + " " + (document.documentElement.getAttribute("data-theme") || "");
        if (/light|white|bright/i.test(className)) {
            newTheme = "light";
        } else {
            var bg = body.style.backgroundColor;
            if (!bg) {
                try { bg = getComputedStyle(body).backgroundColor; } catch(e) {}
            }
            var rgb = bg && bg.match(/[\d.]+/g);
            if (rgb && rgb.length >= 3) {
                var brightness = (parseFloat(rgb[0]) * 299 + parseFloat(rgb[1]) * 587 + parseFloat(rgb[2]) * 114) / 1000;
                newTheme = brightness < 100 ? "dark" : "light";
            }
        }
        if (newTheme !== currentThemeName) {
            currentThemeName = newTheme;
            applyTheme(THEMES[newTheme]);
        }
    }

    applyTheme(THEMES.dark);

    var wrap = document.createElement("div");
    wrap.className = "wce-wrap";

    var panel = document.createElement("div");
    panel.className = "wce-panel";

    var panelInner = document.createElement("div");
    panelInner.className = "wce-panel-inner";
    panelInner.innerHTML =
        '<div class="wce-header"><h3>' + LANG.title + ' <span class="wce-count"><span id="wce-count">0</span> ' + LANG.msgs + '</span></h3></div>' +
        '<div class="wce-body" id="wce-body"><div class="wce-empty">' + LANG.generating + '</div></div>' +
        '<div class="wce-footer"><button class="wce-btn" id="wce-refresh">Refresh</button></div>';

    var tab = document.createElement("div");
    tab.className = "wce-tab";
    var tabTextEl = document.createElement("div");
    tabTextEl.className = "wce-tab-text";
    tabTextEl.textContent = LANG.title;
    tab.innerHTML = '<div class="wce-tab-icon"></div>';
    tab.appendChild(tabTextEl);

    // Buffer zone fills the gap between tab and panel edge
    var buffer = document.createElement("div");
    buffer.className = "wce-buffer";

    panel.appendChild(panelInner);
    wrap.appendChild(panel);
    wrap.appendChild(buffer);
    wrap.appendChild(tab);
    document.body.appendChild(wrap);

    function updateTabText() {
        tabTextEl.textContent = LANG.title;
    }

    var countEl = document.getElementById("wce-count");
    var bodyEl = document.getElementById("wce-body");
    var allItems = [];
    var lastCount = 0;
    var isOpen = false;

    function openPanel() {
        isOpen = true;
        wrap.classList.add("open");
    }

    function closePanel() {
        isOpen = false;
        wrap.classList.remove("open");
    }

    tab.addEventListener("mouseenter", function() {
        openPanel();
    });

    wrap.addEventListener("mouseleave", function() {
        closePanel();
    });

    function findMessages() {
        var results = [];
        var bubbles = document.querySelectorAll("div.chat-bubble");
        for (var i = 0; i < bubbles.length; i++) {
            var text = bubbles[i].textContent || "";
            if (text.length < 5) continue;
            var preview = text.substring(0, 60).trim().replace(/\s+/g, " ");
            if (preview.length < 5) continue;
            results.push({text: preview + (text.length > 60 ? "..." : ""), el: bubbles[i]});
        }
        return results;
    }

    function render() {
        if (!allItems || allItems.length === 0) {
            bodyEl.innerHTML = '<div class="wce-empty">' + LANG.noMessages + '</div>';
            countEl.textContent = "0";
            return;
        }
        countEl.textContent = allItems.length;
        var html = "";
        for (var i = 0; i < allItems.length; i++) {
            var item = allItems[i];
            var isLatest = i === allItems.length - 1;
            var safeText = item.text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            html += '<div class="wce-item' + (isLatest ? " latest" : "") + '" data-idx="' + i + '">' +
                '<span class="wce-num">' + (i + 1) + '</span>' +
                '<span class="wce-preview">' + safeText + '</span>' +
                (isLatest ? '<span class="wce-badge">' + LANG.latest + '</span>' : '') +
                '</div>';
        }
        bodyEl.innerHTML = html;
        bodyEl.scrollTop = bodyEl.scrollHeight;

        var items = bodyEl.querySelectorAll(".wce-item");
        items.forEach(function(itemEl) {
            itemEl.addEventListener("click", function() {
                var idx = parseInt(this.dataset.idx);
                var el = allItems[idx] && allItems[idx].el;
                if (el) {
                    this.classList.add("clicked");
                    setTimeout(function() {
                        itemEl.classList.remove("clicked");
                    }, 400);
                    el.scrollIntoView({behavior: "smooth", block: "center"});
                    el.style.outline = "2px solid " + theme.accent;
                    el.style.outlineOffset = "3px";
                    el.style.transition = "outline 0.3s, outline-offset 0.3s";
                    setTimeout(function() {
                        el.style.outline = "";
                        el.style.outlineOffset = "";
                    }, 1500);
                }
            });
        });
    }

    function showToast(msg) {
        var toast = document.getElementById("wce-toast");
        if (!toast) {
            toast = document.createElement("div");
            toast.id = "wce-toast";
            toast.className = "wce-toast";
            document.body.appendChild(toast);
        }
        toast.textContent = msg;
        setTimeout(function() {
            toast.classList.add("show");
        }, 10);
        setTimeout(function() {
            toast.classList.remove("show");
        }, 2000);
    }

    function checkNew() {
        var count = document.querySelectorAll("div.chat-bubble").length;
        if (count !== lastCount) {
            lastCount = count;
            allItems = findMessages();
            render();
        }
    }

    document.getElementById("wce-refresh").addEventListener("click", function(e) {
        e.stopPropagation();
        allItems = findMessages();
        lastCount = document.querySelectorAll("div.chat-bubble").length;
        render();
        showToast("Refreshed");
    });

    setTimeout(function() {
        allItems = findMessages();
        lastCount = document.querySelectorAll("div.chat-bubble").length;
        render();
        detectTheme();
    }, 2000);

    setInterval(checkNew, 2000);
    new MutationObserver(checkNew).observe(document.body, {childList: true, subtree: true});

    // Fast theme detection
    var themeObserver = new MutationObserver(function(mutations) {
        detectTheme();
    });
    themeObserver.observe(document.body, {attributes: true, attributeFilter: ["class", "style", "data-theme"]});
    themeObserver.observe(document.documentElement, {attributes: true, attributeFilter: ["class", "style", "data-theme"]});
    setInterval(detectTheme, 300);
})();

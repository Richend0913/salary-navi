"""
年収ナビ (Salary Navigator) - Static Site Generator
Generates Japanese salary information pages for programmatic SEO.
"""
import os
import json
from datetime import datetime
from urllib.parse import quote

SITE_URL = "https://richend0913.github.io/salary-navi"
ADSENSE = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6327505164684489" crossorigin="anonymous"></script>'
YEAR = datetime.now().year

# ============================================================
# Job Data: 45 jobs across 5 categories
# ============================================================
CATEGORIES = [
    {
        "name": "IT・エンジニア",
        "slug": "it",
        "jobs": [
            {
                "title": "プログラマー",
                "slug": "programmer",
                "avg": 450,
                "monthly": 28,
                "bonus": 114,
                "ages": {"20代": 350, "30代": 480, "40代": 550, "50代": 580},
                "sizes": {"大企業（1000人以上）": 550, "中企業（300〜999人）": 460, "小企業（300人未満）": 380},
                "qualifications": "基本情報技術者試験、応用情報技術者試験があると有利。未経験からでもスクール経由で就職可能。",
                "career": "プログラマーとしてキャリアをスタートし、3〜5年の経験を積んだ後、システムエンジニアやプロジェクトリーダーへステップアップするのが一般的です。フリーランスとして独立する道もあり、スキル次第で年収800万円以上も可能です。",
                "related": ["システムエンジニア", "Webデザイナー", "AIエンジニア"],
            },
            {
                "title": "システムエンジニア",
                "slug": "system-engineer",
                "avg": 550,
                "monthly": 34,
                "bonus": 142,
                "ages": {"20代": 400, "30代": 560, "40代": 650, "50代": 700},
                "sizes": {"大企業（1000人以上）": 680, "中企業（300〜999人）": 560, "小企業（300人未満）": 450},
                "qualifications": "応用情報技術者試験、データベーススペシャリスト、プロジェクトマネージャ試験など。",
                "career": "プログラマーから転身するケースが多く、要件定義・設計・テストまで幅広く担当します。上流工程の経験を積むことでPMやITコンサルタントへのキャリアパスが開けます。",
                "related": ["プログラマー", "プロジェクトマネージャー", "インフラエンジニア"],
            },
            {
                "title": "Webデザイナー",
                "slug": "web-designer",
                "avg": 380,
                "monthly": 24,
                "bonus": 92,
                "ages": {"20代": 300, "30代": 400, "40代": 450, "50代": 460},
                "sizes": {"大企業（1000人以上）": 480, "中企業（300〜999人）": 390, "小企業（300人未満）": 320},
                "qualifications": "ウェブデザイン技能検定、色彩検定、Adobe認定資格など。ポートフォリオが最重要。",
                "career": "Webデザイナーからアートディレクター、UI/UXデザイナーへのキャリアアップが一般的です。フロントエンド開発スキルを習得することで市場価値が大幅に向上します。",
                "related": ["プログラマー", "データサイエンティスト", "AIエンジニア"],
            },
            {
                "title": "データサイエンティスト",
                "slug": "data-scientist",
                "avg": 700,
                "monthly": 44,
                "bonus": 172,
                "ages": {"20代": 500, "30代": 720, "40代": 850, "50代": 900},
                "sizes": {"大企業（1000人以上）": 850, "中企業（300〜999人）": 700, "小企業（300人未満）": 550},
                "qualifications": "統計検定2級以上、Python・R言語のスキル、修士・博士号があると有利。G検定、E資格など。",
                "career": "データ分析の実務経験を積み、シニアデータサイエンティストやチーフデータオフィサー(CDO)を目指すキャリアパスがあります。AI・機械学習の専門性を高めることで年収1000万円超えも珍しくありません。",
                "related": ["AIエンジニア", "プログラマー", "システムエンジニア"],
            },
            {
                "title": "インフラエンジニア",
                "slug": "infra-engineer",
                "avg": 520,
                "monthly": 33,
                "bonus": 124,
                "ages": {"20代": 380, "30代": 530, "40代": 620, "50代": 650},
                "sizes": {"大企業（1000人以上）": 640, "中企業（300〜999人）": 530, "小企業（300人未満）": 420},
                "qualifications": "CCNA、LPIC、AWS認定ソリューションアーキテクト、情報処理安全確保支援士など。",
                "career": "サーバー・ネットワークの運用保守からスタートし、設計・構築へとステップアップ。クラウドエンジニアやセキュリティエンジニアとして専門性を高めるキャリアパスが人気です。",
                "related": ["システムエンジニア", "プロジェクトマネージャー", "プログラマー"],
            },
            {
                "title": "プロジェクトマネージャー",
                "slug": "project-manager",
                "avg": 680,
                "monthly": 43,
                "bonus": 164,
                "ages": {"20代": 450, "30代": 650, "40代": 780, "50代": 820},
                "sizes": {"大企業（1000人以上）": 850, "中企業（300〜999人）": 680, "小企業（300人未満）": 550},
                "qualifications": "プロジェクトマネージャ試験（IPA）、PMP（Project Management Professional）、ITストラテジスト。",
                "career": "SE・プログラマーとして5〜10年の実務経験を積んだ後にPMへ転身するのが王道ルートです。大規模プロジェクトの管理経験を積むことで、IT部門長やCTOへのキャリアパスが開けます。",
                "related": ["システムエンジニア", "インフラエンジニア", "データサイエンティスト"],
            },
            {
                "title": "AIエンジニア",
                "slug": "ai-engineer",
                "avg": 750,
                "monthly": 47,
                "bonus": 186,
                "ages": {"20代": 550, "30代": 780, "40代": 900, "50代": 950},
                "sizes": {"大企業（1000人以上）": 920, "中企業（300〜999人）": 750, "小企業（300人未満）": 600},
                "qualifications": "E資格、G検定、Python・TensorFlow・PyTorchのスキル。修士・博士号があると大幅に有利。",
                "career": "機械学習エンジニアとして経験を積み、AIアーキテクトやリサーチサイエンティストへ進むキャリアパスがあります。GAFAMなど外資系企業では年収1500万円以上のオファーも珍しくありません。",
                "related": ["データサイエンティスト", "プログラマー", "システムエンジニア"],
            },
            {
                "title": "ネットワークエンジニア",
                "slug": "network-engineer",
                "avg": 490,
                "monthly": 31,
                "bonus": 118,
                "ages": {"20代": 370, "30代": 500, "40代": 580, "50代": 600},
                "sizes": {"大企業（1000人以上）": 600, "中企業（300〜999人）": 500, "小企業（300人未満）": 400},
                "qualifications": "CCNA、CCNP、ネットワークスペシャリスト試験、情報処理安全確保支援士。",
                "career": "ネットワークの監視・運用からスタートし、設計・構築へとキャリアアップ。セキュリティやクラウドの専門性を掛け合わせることで、市場価値をさらに高められます。",
                "related": ["インフラエンジニア", "システムエンジニア", "プログラマー"],
            },
            {
                "title": "ITコンサルタント",
                "slug": "it-consultant",
                "avg": 800,
                "monthly": 50,
                "bonus": 200,
                "ages": {"20代": 550, "30代": 800, "40代": 950, "50代": 1000},
                "sizes": {"大企業（1000人以上）": 1000, "中企業（300〜999人）": 800, "小企業（300人未満）": 650},
                "qualifications": "ITストラテジスト、中小企業診断士、PMP。MBA取得者も多い。",
                "career": "SEやPMとして実務経験を積んだ後、コンサルティングファームに転職するのが一般的なルートです。マネージャー、シニアマネージャー、パートナーと昇進し、パートナークラスでは年収2000万円以上になります。",
                "related": ["プロジェクトマネージャー", "システムエンジニア", "データサイエンティスト"],
            },
        ],
    },
    {
        "name": "医療・福祉",
        "slug": "medical",
        "jobs": [
            {
                "title": "医師",
                "slug": "doctor",
                "avg": 1200,
                "monthly": 80,
                "bonus": 240,
                "ages": {"20代": 650, "30代": 1100, "40代": 1400, "50代": 1600},
                "sizes": {"大企業（1000人以上）": 1400, "中企業（300〜999人）": 1200, "小企業（300人未満）": 1000},
                "qualifications": "医師免許（国家試験合格が必須）。医学部6年+臨床研修2年が最低限必要。",
                "career": "臨床研修を経て専門医を取得し、勤務医として経験を積みます。開業医になると年収2000万円以上も可能。大学病院の教授や病院長を目指すアカデミックキャリアもあります。",
                "related": ["歯科医師", "薬剤師", "看護師"],
            },
            {
                "title": "看護師",
                "slug": "nurse",
                "avg": 500,
                "monthly": 33,
                "bonus": 104,
                "ages": {"20代": 400, "30代": 490, "40代": 540, "50代": 560},
                "sizes": {"大企業（1000人以上）": 560, "中企業（300〜999人）": 500, "小企業（300人未満）": 430},
                "qualifications": "看護師国家資格（看護学校3年または大学4年卒業後に受験）。准看護師からステップアップも可能。",
                "career": "病棟勤務から主任、師長へとキャリアアップするのが一般的です。認定看護師や専門看護師の資格を取得することで、専門性と給与の両方を高められます。",
                "related": ["医師", "薬剤師", "理学療法士"],
            },
            {
                "title": "薬剤師",
                "slug": "pharmacist",
                "avg": 580,
                "monthly": 37,
                "bonus": 136,
                "ages": {"20代": 420, "30代": 570, "40代": 650, "50代": 700},
                "sizes": {"大企業（1000人以上）": 680, "中企業（300〜999人）": 580, "小企業（300人未満）": 500},
                "qualifications": "薬剤師国家資格（薬学部6年制卒業後に受験）。",
                "career": "調剤薬局、病院、ドラッグストア、製薬会社など活躍の場は幅広いです。管理薬剤師になると手当が加算され、独立開業で年収1000万円以上を目指すことも可能です。",
                "related": ["医師", "看護師", "歯科医師"],
            },
            {
                "title": "歯科医師",
                "slug": "dentist",
                "avg": 800,
                "monthly": 53,
                "bonus": 164,
                "ages": {"20代": 450, "30代": 750, "40代": 950, "50代": 1050},
                "sizes": {"大企業（1000人以上）": 900, "中企業（300〜999人）": 800, "小企業（300人未満）": 700},
                "qualifications": "歯科医師国家資格（歯学部6年卒業後に受験）。",
                "career": "勤務医として経験を積んだ後、開業するケースが多いです。自由診療（審美歯科・インプラント等）を取り入れることで高収入を得ることも可能です。",
                "related": ["医師", "薬剤師", "看護師"],
            },
            {
                "title": "理学療法士",
                "slug": "physical-therapist",
                "avg": 420,
                "monthly": 27,
                "bonus": 96,
                "ages": {"20代": 340, "30代": 420, "40代": 480, "50代": 500},
                "sizes": {"大企業（1000人以上）": 480, "中企業（300〜999人）": 420, "小企業（300人未満）": 370},
                "qualifications": "理学療法士国家資格（養成校3〜4年卒業後に受験）。",
                "career": "病院やリハビリ施設で経験を積み、主任・科長へ昇進するキャリアパスがあります。スポーツ分野や訪問リハビリなど専門特化することで市場価値を高められます。",
                "related": ["看護師", "医師", "保育士"],
            },
            {
                "title": "臨床検査技師",
                "slug": "clinical-lab-tech",
                "avg": 460,
                "monthly": 29,
                "bonus": 112,
                "ages": {"20代": 360, "30代": 460, "40代": 520, "50代": 540},
                "sizes": {"大企業（1000人以上）": 530, "中企業（300〜999人）": 460, "小企業（300人未満）": 400},
                "qualifications": "臨床検査技師国家資格。超音波検査士、細胞検査士などの専門資格も有利。",
                "career": "病院の検査室で経験を積み、技師長を目指すキャリアパスがあります。超音波検査や遺伝子検査など専門分野を持つことで需要が高まります。",
                "related": ["薬剤師", "看護師", "理学療法士"],
            },
        ],
    },
    {
        "name": "金融・会計",
        "slug": "finance",
        "jobs": [
            {
                "title": "銀行員",
                "slug": "banker",
                "avg": 620,
                "monthly": 39,
                "bonus": 152,
                "ages": {"20代": 420, "30代": 600, "40代": 750, "50代": 800},
                "sizes": {"大企業（1000人以上）": 800, "中企業（300〜999人）": 600, "小企業（300人未満）": 480},
                "qualifications": "銀行業務検定、FP技能士、証券外務員資格、宅地建物取引士など。",
                "career": "窓口業務や融資業務からスタートし、支店長、エリアマネージャーへと昇進するキャリアパスがあります。メガバンクでは部長クラスで年収1500万円以上になることも。",
                "related": ["証券アナリスト", "ファイナンシャルプランナー", "公認会計士"],
            },
            {
                "title": "証券アナリスト",
                "slug": "securities-analyst",
                "avg": 800,
                "monthly": 50,
                "bonus": 200,
                "ages": {"20代": 550, "30代": 800, "40代": 1000, "50代": 1100},
                "sizes": {"大企業（1000人以上）": 1050, "中企業（300〜999人）": 800, "小企業（300人未満）": 650},
                "qualifications": "証券アナリスト資格（CMA）、CFA（米国証券アナリスト）。",
                "career": "リサーチアナリストとしてスタートし、シニアアナリスト、チーフストラテジストへと昇進します。外資系証券では年収2000万円以上のポジションも多く存在します。",
                "related": ["銀行員", "ファイナンシャルプランナー", "公認会計士"],
            },
            {
                "title": "ファイナンシャルプランナー",
                "slug": "financial-planner",
                "avg": 500,
                "monthly": 32,
                "bonus": 116,
                "ages": {"20代": 350, "30代": 490, "40代": 580, "50代": 600},
                "sizes": {"大企業（1000人以上）": 600, "中企業（300〜999人）": 500, "小企業（300人未満）": 400},
                "qualifications": "FP技能士2級以上（国家資格）、AFP・CFP（民間資格）。",
                "career": "保険会社や銀行でFP業務の経験を積んだ後、独立系FPとして開業する道があります。顧客基盤を築けば年収1000万円以上も十分に狙えます。",
                "related": ["銀行員", "証券アナリスト", "不動産営業"],
            },
            {
                "title": "公認会計士",
                "slug": "accountant",
                "avg": 900,
                "monthly": 56,
                "bonus": 228,
                "ages": {"20代": 550, "30代": 850, "40代": 1050, "50代": 1150},
                "sizes": {"大企業（1000人以上）": 1100, "中企業（300〜999人）": 900, "小企業（300人未満）": 700},
                "qualifications": "公認会計士試験合格（合格率約10%の難関資格）。",
                "career": "監査法人でスタッフ、シニア、マネージャー、パートナーと昇進するのが王道です。パートナーになると年収2000万円以上。独立開業やコンサルティングへの転身も多いです。",
                "related": ["証券アナリスト", "銀行員", "ファイナンシャルプランナー"],
            },
            {
                "title": "税理士",
                "slug": "tax-accountant",
                "avg": 720,
                "monthly": 45,
                "bonus": 180,
                "ages": {"20代": 400, "30代": 650, "40代": 850, "50代": 950},
                "sizes": {"大企業（1000人以上）": 880, "中企業（300〜999人）": 720, "小企業（300人未満）": 580},
                "qualifications": "税理士試験5科目合格（科目合格制）。大学院修了による一部免除制度あり。",
                "career": "税理士法人や会計事務所で実務経験を積んだ後、独立開業するのが王道のキャリアパスです。顧問先を増やすことで年収1500万円以上を目指せます。",
                "related": ["公認会計士", "銀行員", "ファイナンシャルプランナー"],
            },
            {
                "title": "アクチュアリー",
                "slug": "actuary",
                "avg": 1000,
                "monthly": 63,
                "bonus": 244,
                "ages": {"20代": 650, "30代": 1000, "40代": 1200, "50代": 1300},
                "sizes": {"大企業（1000人以上）": 1200, "中企業（300〜999人）": 950, "小企業（300人未満）": 800},
                "qualifications": "日本アクチュアリー会の資格試験（全科目合格まで平均8年）。数学・統計学の高度な知識が必須。",
                "career": "保険会社や信託銀行で商品開発・リスク管理に従事します。チーフアクチュアリーやCRO（最高リスク管理責任者）への昇進が可能で、外資系では年収2000万円以上のポジションもあります。",
                "related": ["証券アナリスト", "公認会計士", "データサイエンティスト"],
            },
        ],
    },
    {
        "name": "公務員・教育",
        "slug": "public",
        "jobs": [
            {
                "title": "国家公務員",
                "slug": "national-civil-servant",
                "avg": 680,
                "monthly": 42,
                "bonus": 176,
                "ages": {"20代": 420, "30代": 620, "40代": 780, "50代": 850},
                "sizes": {"大企業（1000人以上）": 680, "中企業（300〜999人）": 680, "小企業（300人未満）": 680},
                "qualifications": "国家公務員採用試験（総合職・一般職）合格。総合職は旧国家I種に相当する難関。",
                "career": "係員→主任→係長→課長補佐→課長→審議官→局長と昇進します。総合職（キャリア）は昇進が早く、局長クラスで年収1500万円以上。退職後の再就職先も安定しています。",
                "related": ["地方公務員", "教師", "警察官"],
            },
            {
                "title": "地方公務員",
                "slug": "local-civil-servant",
                "avg": 630,
                "monthly": 40,
                "bonus": 150,
                "ages": {"20代": 380, "30代": 560, "40代": 720, "50代": 780},
                "sizes": {"大企業（1000人以上）": 650, "中企業（300〜999人）": 630, "小企業（300人未満）": 600},
                "qualifications": "地方公務員採用試験合格（上級・中級・初級）。自治体により試験内容が異なる。",
                "career": "主事→主任→係長→課長→部長へと昇進するのが一般的です。福利厚生が充実しており、安定した待遇が魅力。ワークライフバランスを重視する人に人気です。",
                "related": ["国家公務員", "教師", "消防士"],
            },
            {
                "title": "警察官",
                "slug": "police-officer",
                "avg": 700,
                "monthly": 44,
                "bonus": 172,
                "ages": {"20代": 450, "30代": 650, "40代": 800, "50代": 850},
                "sizes": {"大企業（1000人以上）": 700, "中企業（300〜999人）": 700, "小企業（300人未満）": 700},
                "qualifications": "各都道府県警察の採用試験合格。警察学校での研修（6〜10ヶ月）を修了する必要あり。",
                "career": "巡査→巡査部長→警部補→警部→警視と昇進します。刑事、交通、警備などの専門部署への配属も。幹部候補はキャリア組（国家公務員総合職）で採用されます。",
                "related": ["消防士", "国家公務員", "地方公務員"],
            },
            {
                "title": "消防士",
                "slug": "firefighter",
                "avg": 640,
                "monthly": 40,
                "bonus": 160,
                "ages": {"20代": 420, "30代": 600, "40代": 740, "50代": 780},
                "sizes": {"大企業（1000人以上）": 660, "中企業（300〜999人）": 640, "小企業（300人未満）": 620},
                "qualifications": "各自治体の消防職採用試験合格。消防学校での研修（約6ヶ月）を修了する必要あり。体力試験が重要。",
                "career": "消防士→消防士長→消防司令補→消防司令→消防監と階級が上がります。救急救命士や予防技術資格者などの専門資格を取得することでキャリアの幅が広がります。",
                "related": ["警察官", "地方公務員", "国家公務員"],
            },
            {
                "title": "教師",
                "slug": "teacher",
                "avg": 620,
                "monthly": 39,
                "bonus": 152,
                "ages": {"20代": 380, "30代": 560, "40代": 720, "50代": 780},
                "sizes": {"大企業（1000人以上）": 640, "中企業（300〜999人）": 620, "小企業（300人未満）": 580},
                "qualifications": "教員免許状（大学で教職課程を履修して取得）。教員採用試験に合格する必要あり。",
                "career": "教諭としてスタートし、主幹教諭、教頭、校長へと管理職を目指すキャリアパスがあります。教育委員会への異動や指導主事としての行政キャリアもあります。",
                "related": ["地方公務員", "保育士", "国家公務員"],
            },
            {
                "title": "大学教授",
                "slug": "university-professor",
                "avg": 1050,
                "monthly": 66,
                "bonus": 258,
                "ages": {"20代": 450, "30代": 700, "40代": 1000, "50代": 1200},
                "sizes": {"大企業（1000人以上）": 1100, "中企業（300〜999人）": 1000, "小企業（300人未満）": 850},
                "qualifications": "博士号（Ph.D.）が事実上必須。研究業績（論文数・引用数）が重要な評価基準。",
                "career": "助教→講師→准教授→教授と昇進します。任期付きポジションが増加傾向にあり、テニュア（終身在職権）獲得が大きな節目です。",
                "related": ["教師", "データサイエンティスト", "医師"],
            },
        ],
    },
    {
        "name": "その他専門職",
        "slug": "other",
        "jobs": [
            {
                "title": "弁護士",
                "slug": "lawyer",
                "avg": 1000,
                "monthly": 63,
                "bonus": 244,
                "ages": {"20代": 600, "30代": 950, "40代": 1200, "50代": 1350},
                "sizes": {"大企業（1000人以上）": 1300, "中企業（300〜999人）": 1000, "小企業（300人未満）": 750},
                "qualifications": "司法試験合格、司法修習修了。法科大学院（ロースクール）修了または予備試験合格が受験要件。",
                "career": "法律事務所のアソシエイトとしてスタートし、パートナーを目指すのが王道です。四大法律事務所ではパートナーで年収3000万円以上。企業内弁護士（インハウス）も増加しています。",
                "related": ["公認会計士", "国家公務員", "税理士"],
            },
            {
                "title": "建築士",
                "slug": "architect",
                "avg": 600,
                "monthly": 38,
                "bonus": 144,
                "ages": {"20代": 400, "30代": 580, "40代": 700, "50代": 730},
                "sizes": {"大企業（1000人以上）": 750, "中企業（300〜999人）": 600, "小企業（300人未満）": 480},
                "qualifications": "一級建築士（国家資格・合格率約10%）、二級建築士。実務経験が受験要件。",
                "career": "設計事務所やゼネコンで実務経験を積み、一級建築士を取得後に独立するケースが多いです。著名建築家になると年収数千万円も可能ですが、平均的な独立建築士の収入は地域差が大きいです。",
                "related": ["不動産営業", "プロジェクトマネージャー", "インフラエンジニア"],
            },
            {
                "title": "パイロット",
                "slug": "pilot",
                "avg": 1500,
                "monthly": 94,
                "bonus": 372,
                "ages": {"20代": 800, "30代": 1400, "40代": 1700, "50代": 1800},
                "sizes": {"大企業（1000人以上）": 1700, "中企業（300〜999人）": 1400, "小企業（300人未満）": 1100},
                "qualifications": "事業用操縦士免許、定期運送用操縦士免許、航空身体検査証明。航空大学校またはエアラインの自社養成課程で訓練。",
                "career": "副操縦士としてスタートし、機長へ昇格するのに通常10年程度かかります。大手航空会社の機長は年収2000万円前後。LCCでは待遇が異なります。",
                "related": ["国家公務員", "医師", "弁護士"],
            },
            {
                "title": "美容師",
                "slug": "hairdresser",
                "avg": 330,
                "monthly": 22,
                "bonus": 66,
                "ages": {"20代": 270, "30代": 340, "40代": 380, "50代": 390},
                "sizes": {"大企業（1000人以上）": 400, "中企業（300〜999人）": 340, "小企業（300人未満）": 280},
                "qualifications": "美容師免許（国家資格）。美容専門学校（2年制）卒業後に受験。",
                "career": "アシスタント→スタイリスト→トップスタイリスト→店長と昇進するのが一般的です。独立開業やフリーランスとして活躍する美容師も多く、カリスマ美容師は年収1000万円以上稼ぐケースもあります。",
                "related": ["保育士", "看護師", "Webデザイナー"],
            },
            {
                "title": "保育士",
                "slug": "nursery-teacher",
                "avg": 380,
                "monthly": 24,
                "bonus": 92,
                "ages": {"20代": 310, "30代": 370, "40代": 420, "50代": 440},
                "sizes": {"大企業（1000人以上）": 430, "中企業（300〜999人）": 380, "小企業（300人未満）": 330},
                "qualifications": "保育士資格（保育士養成施設卒業または保育士試験合格）。",
                "career": "保育士として経験を積み、主任保育士、園長へとキャリアアップします。近年は処遇改善加算により給与水準が上昇傾向にあります。児童発達支援など専門分野への転身も可能です。",
                "related": ["教師", "看護師", "理学療法士"],
            },
            {
                "title": "不動産営業",
                "slug": "real-estate-sales",
                "avg": 520,
                "monthly": 33,
                "bonus": 124,
                "ages": {"20代": 380, "30代": 530, "40代": 620, "50代": 600},
                "sizes": {"大企業（1000人以上）": 700, "中企業（300〜999人）": 520, "小企業（300人未満）": 400},
                "qualifications": "宅地建物取引士（国家資格）がほぼ必須。FP技能士、マンション管理士もあると有利。",
                "career": "営業職からスタートし、営業所長、支店長へと昇進するキャリアパスがあります。成果報酬型の企業では、トップセールスで年収1000万円以上も十分可能です。",
                "related": ["ファイナンシャルプランナー", "銀行員", "建築士"],
            },
            {
                "title": "薬品メーカーMR",
                "slug": "mr",
                "avg": 650,
                "monthly": 41,
                "bonus": 158,
                "ages": {"20代": 480, "30代": 650, "40代": 750, "50代": 780},
                "sizes": {"大企業（1000人以上）": 780, "中企業（300〜999人）": 640, "小企業（300人未満）": 520},
                "qualifications": "MR認定試験合格。薬学部卒が有利だが、文系出身者も多い。普通自動車免許必須。",
                "career": "MRとして医療機関への営業を行い、エリアマネージャー、支店長へとキャリアアップします。マーケティング部門や本社企画部門への異動もあります。",
                "related": ["薬剤師", "医師", "不動産営業"],
            },
            {
                "title": "社会保険労務士",
                "slug": "labor-consultant",
                "avg": 550,
                "monthly": 35,
                "bonus": 130,
                "ages": {"20代": 350, "30代": 500, "40代": 650, "50代": 700},
                "sizes": {"大企業（1000人以上）": 680, "中企業（300〜999人）": 550, "小企業（300人未満）": 430},
                "qualifications": "社会保険労務士試験合格（合格率約6%の難関資格）。",
                "career": "社労士事務所や企業の人事部で実務経験を積んだ後、独立開業するのが王道です。顧問先を増やすことで年収1000万円以上を目指せます。企業内社労士として人事のスペシャリストになる道もあります。",
                "related": ["公認会計士", "税理士", "弁護士"],
            },
            {
                "title": "司法書士",
                "slug": "judicial-scrivener",
                "avg": 630,
                "monthly": 40,
                "bonus": 150,
                "ages": {"20代": 380, "30代": 580, "40代": 750, "50代": 800},
                "sizes": {"大企業（1000人以上）": 750, "中企業（300〜999人）": 630, "小企業（300人未満）": 500},
                "qualifications": "司法書士試験合格（合格率約4%の超難関資格）。",
                "career": "司法書士事務所で実務経験を積み、独立開業するのが一般的です。不動産登記や会社登記の需要は安定しており、簡裁代理権を取得すれば業務の幅がさらに広がります。",
                "related": ["弁護士", "税理士", "不動産営業"],
            },
            {
                "title": "管理栄養士",
                "slug": "dietitian",
                "avg": 400,
                "monthly": 26,
                "bonus": 88,
                "ages": {"20代": 320, "30代": 390, "40代": 440, "50代": 460},
                "sizes": {"大企業（1000人以上）": 460, "中企業（300〜999人）": 400, "小企業（300人未満）": 350},
                "qualifications": "管理栄養士国家資格（管理栄養士養成課程を卒業後に受験）。",
                "career": "病院、学校、福祉施設、食品メーカーなど活躍の場は幅広いです。栄養指導のスペシャリストとしてのキャリアを積むか、フードコンサルタントとして独立する道もあります。",
                "related": ["看護師", "薬剤師", "保育士"],
            },
            {
                "title": "公認心理師",
                "slug": "psychologist",
                "avg": 420,
                "monthly": 27,
                "bonus": 96,
                "ages": {"20代": 320, "30代": 410, "40代": 480, "50代": 500},
                "sizes": {"大企業（1000人以上）": 490, "中企業（300〜999人）": 420, "小企業（300人未満）": 360},
                "qualifications": "公認心理師国家資格（2017年創設）。大学院修了が一般的なルート。臨床心理士との併有が望ましい。",
                "career": "病院、学校、企業のメンタルヘルス部門など活躍の場が広がっています。スクールカウンセラーや産業カウンセラーとして専門性を高めるキャリアパスがあります。",
                "related": ["看護師", "教師", "保育士"],
            },
            {
                "title": "行政書士",
                "slug": "administrative-scrivener",
                "avg": 500,
                "monthly": 32,
                "bonus": 116,
                "ages": {"20代": 320, "30代": 460, "40代": 580, "50代": 620},
                "sizes": {"大企業（1000人以上）": 580, "中企業（300〜999人）": 500, "小企業（300人未満）": 400},
                "qualifications": "行政書士試験合格（合格率約10〜12%）。法学部出身者に有利。",
                "career": "行政書士事務所で実務経験を積んだ後に独立開業するのが一般的です。入管業務や建設業許可など専門分野に特化することで高収入を得ることも可能です。",
                "related": ["司法書士", "弁護士", "社会保険労務士"],
            },
            {
                "title": "電気工事士",
                "slug": "electrician",
                "avg": 430,
                "monthly": 28,
                "bonus": 94,
                "ages": {"20代": 330, "30代": 420, "40代": 490, "50代": 510},
                "sizes": {"大企業（1000人以上）": 530, "中企業（300〜999人）": 430, "小企業（300人未満）": 370},
                "qualifications": "第二種電気工事士（国家資格）。第一種電気工事士、電気主任技術者を取得するとキャリアアップに有利。",
                "career": "電気工事会社で技術を磨き、現場監督や工事管理者へとキャリアアップします。独立して電気工事業を開業することも可能で、人手不足が続く業界のため需要は安定しています。",
                "related": ["建築士", "インフラエンジニア", "消防士"],
            },
            {
                "title": "Webマーケター",
                "slug": "web-marketer",
                "avg": 530,
                "monthly": 33,
                "bonus": 134,
                "ages": {"20代": 380, "30代": 540, "40代": 630, "50代": 650},
                "sizes": {"大企業（1000人以上）": 660, "中企業（300〜999人）": 530, "小企業（300人未満）": 420},
                "qualifications": "Google広告認定資格、Google Analytics認定資格、ウェブ解析士など。実績とスキルが最重要。",
                "career": "広告運用やSEOの実務経験を積み、マーケティングマネージャーやCMO（最高マーケティング責任者）を目指すキャリアパスがあります。フリーランスとして独立する人も多い業界です。",
                "related": ["Webデザイナー", "プログラマー", "データサイエンティスト"],
            },
            {
                "title": "獣医師",
                "slug": "veterinarian",
                "avg": 650,
                "monthly": 41,
                "bonus": 158,
                "ages": {"20代": 420, "30代": 620, "40代": 750, "50代": 800},
                "sizes": {"大企業（1000人以上）": 750, "中企業（300〜999人）": 650, "小企業（300人未満）": 550},
                "qualifications": "獣医師国家資格（獣医学部6年制卒業後に受験）。",
                "career": "動物病院での勤務医からスタートし、開業獣医師を目指すのが王道です。ペット需要の増加により動物病院の経営は比較的安定しています。公務員獣医師（食品衛生・家畜防疫）の道もあります。",
                "related": ["医師", "薬剤師", "看護師"],
            },
            {
                "title": "通訳・翻訳",
                "slug": "interpreter",
                "avg": 480,
                "monthly": 30,
                "bonus": 120,
                "ages": {"20代": 350, "30代": 470, "40代": 550, "50代": 570},
                "sizes": {"大企業（1000人以上）": 580, "中企業（300〜999人）": 480, "小企業（300人未満）": 390},
                "qualifications": "TOEIC900点以上、英検1級、通訳案内士（国家資格）など。専門分野の知識も重要。",
                "career": "翻訳会社や企業の国際部門で経験を積み、フリーランスとして独立するケースが多いです。医療翻訳や特許翻訳など専門分野に特化すると単価が大幅に上がります。会議通訳の日給は5〜10万円が相場です。",
                "related": ["教師", "Webマーケター", "ITコンサルタント"],
            },
            {
                "title": "調理師",
                "slug": "chef",
                "avg": 360,
                "monthly": 23,
                "bonus": 84,
                "ages": {"20代": 280, "30代": 350, "40代": 400, "50代": 420},
                "sizes": {"大企業（1000人以上）": 420, "中企業（300〜999人）": 360, "小企業（300人未満）": 300},
                "qualifications": "調理師免許（養成施設卒業または実務経験2年+試験合格）。ふぐ調理師免許、製菓衛生師なども有利。",
                "career": "調理補助からスタートし、各セクションのシェフ、スーシェフ、総料理長へとキャリアアップします。独立開業や、ホテル・レストランの料理長ポジションを目指すのが一般的です。",
                "related": ["管理栄養士", "美容師", "保育士"],
            },
        ],
    },
]

# Build flat lookup
ALL_JOBS = {}
for cat in CATEGORIES:
    for job in cat["jobs"]:
        ALL_JOBS[job["title"]] = job


def fmt(n):
    """Format number with commas."""
    return f"{n:,}"


def slug_for_title(title):
    """Get slug for a job title."""
    if title in ALL_JOBS:
        return ALL_JOBS[title]["slug"]
    return None


# Affiliate settings
AMAZON_TAG = "okuritegift-22"
RAKUTEN_AFF_ID = "522e40a0.f2dc4208.522e40a1.385f875e"

# Per-job affiliate keywords: (amazon_book_keywords, rakuten_study_keywords, skill_amazon_keywords, skill_rakuten_keywords)
AFFILIATE_KEYWORDS = {
    "プログラマー": ("プログラマー 転職 本", "プログラミング 資格 教材", "プログラミング 入門 本", "プログラミング 学習 教材"),
    "システムエンジニア": ("システムエンジニア 転職 本", "応用情報技術者 テキスト", "SE 設計 入門 本", "情報処理技術者 教材"),
    "Webデザイナー": ("Webデザイナー 転職 本", "ウェブデザイン技能検定 テキスト", "Webデザイン 入門 本", "デザイン 学習 教材"),
    "データサイエンティスト": ("データサイエンティスト 転職 本", "統計検定 テキスト", "データサイエンス 入門 本", "Python データ分析 教材"),
    "インフラエンジニア": ("インフラエンジニア 転職 本", "AWS認定 テキスト", "ネットワーク サーバー 入門 本", "LPIC 教材"),
    "プロジェクトマネージャー": ("プロジェクトマネージャー 転職 本", "PMP テキスト", "プロジェクトマネジメント 入門 本", "プロジェクトマネージャ試験 教材"),
    "AIエンジニア": ("AIエンジニア 転職 本", "E資格 テキスト", "機械学習 深層学習 入門 本", "AI 人工知能 学習 教材"),
    "ネットワークエンジニア": ("ネットワークエンジニア 転職 本", "CCNA テキスト", "ネットワーク 入門 本", "ネットワークスペシャリスト 教材"),
    "ITコンサルタント": ("ITコンサルタント 転職 本", "ITストラテジスト テキスト", "コンサルタント 入門 本", "中小企業診断士 教材"),
    "医師": ("医師 キャリア 本", "医師国家試験 テキスト", "医学 入門 本", "医師国家試験 教材"),
    "看護師": ("看護師 転職 本", "看護師国家試験 テキスト", "看護 入門 本", "看護師 資格 教材"),
    "薬剤師": ("薬剤師 転職 本", "薬剤師国家試験 テキスト", "薬学 入門 本", "薬剤師 資格 教材"),
    "歯科医師": ("歯科医師 キャリア 本", "歯科医師国家試験 テキスト", "歯科 入門 本", "歯科医師 資格 教材"),
    "理学療法士": ("理学療法士 転職 本", "理学療法士国家試験 テキスト", "リハビリテーション 入門 本", "理学療法士 資格 教材"),
    "臨床検査技師": ("臨床検査技師 転職 本", "臨床検査技師国家試験 テキスト", "臨床検査 入門 本", "臨床検査技師 資格 教材"),
    "銀行員": ("銀行員 転職 本", "銀行業務検定 テキスト", "金融 入門 本", "FP技能士 教材"),
    "証券アナリスト": ("証券アナリスト 転職 本", "証券アナリスト CMA テキスト", "証券分析 入門 本", "証券アナリスト 資格 教材"),
    "ファイナンシャルプランナー": ("ファイナンシャルプランナー 転職 本", "FP技能士 テキスト", "FP 入門 本", "ファイナンシャルプランナー 資格 教材"),
    "公認会計士": ("公認会計士 転職 本", "公認会計士試験 テキスト", "会計 入門 本", "公認会計士 資格 教材"),
    "税理士": ("税理士 転職 本", "税理士試験 テキスト", "税務 入門 本", "税理士 資格 教材"),
    "アクチュアリー": ("アクチュアリー キャリア 本", "アクチュアリー試験 テキスト", "保険数学 入門 本", "アクチュアリー 資格 教材"),
    "国家公務員": ("国家公務員 転職 本", "国家公務員試験 テキスト", "公務員 入門 本", "公務員試験 教材"),
    "地方公務員": ("地方公務員 転職 本", "地方公務員試験 テキスト", "公務員 入門 本", "地方公務員試験 教材"),
    "警察官": ("警察官 採用 本", "警察官採用試験 テキスト", "警察 入門 本", "警察官 試験 教材"),
    "消防士": ("消防士 採用 本", "消防士採用試験 テキスト", "消防 入門 本", "消防士 試験 教材"),
    "教師": ("教師 転職 本", "教員採用試験 テキスト", "教育 入門 本", "教員採用試験 教材"),
    "大学教授": ("大学教授 キャリア 本", "博士課程 研究 テキスト", "研究者 入門 本", "アカデミア 研究 教材"),
    "弁護士": ("弁護士 転職 本", "司法試験 テキスト", "法律 入門 本", "司法試験 教材"),
    "建築士": ("建築士 転職 本", "一級建築士 テキスト", "建築 入門 本", "建築士 資格 教材"),
    "パイロット": ("パイロット キャリア 本", "航空 操縦士 テキスト", "航空 入門 本", "パイロット 資格 教材"),
    "美容師": ("美容師 転職 本", "美容師国家試験 テキスト", "美容 入門 本", "美容師 資格 教材"),
    "保育士": ("保育士 転職 本", "保育士試験 テキスト", "保育 入門 本", "保育士 資格 教材"),
    "不動産営業": ("不動産 転職 本", "宅建 テキスト", "不動産 入門 本", "宅地建物取引士 教材"),
    "薬品メーカーMR": ("MR 転職 本", "MR認定試験 テキスト", "製薬 MR 入門 本", "MR認定 資格 教材"),
    "社会保険労務士": ("社労士 転職 本", "社会保険労務士試験 テキスト", "社労士 入門 本", "社労士 資格 教材"),
    "司法書士": ("司法書士 転職 本", "司法書士試験 テキスト", "司法書士 入門 本", "司法書士 資格 教材"),
    "管理栄養士": ("管理栄養士 転職 本", "管理栄養士国家試験 テキスト", "栄養学 入門 本", "管理栄養士 資格 教材"),
    "公認心理師": ("公認心理師 転職 本", "公認心理師試験 テキスト", "心理学 入門 本", "公認心理師 資格 教材"),
    "行政書士": ("行政書士 転職 本", "行政書士試験 テキスト", "行政書士 入門 本", "行政書士 資格 教材"),
    "電気工事士": ("電気工事士 転職 本", "電気工事士試験 テキスト", "電気工事 入門 本", "電気工事士 資格 教材"),
    "Webマーケター": ("Webマーケター 転職 本", "ウェブ解析士 テキスト", "Webマーケティング 入門 本", "デジタルマーケティング 教材"),
    "獣医師": ("獣医師 キャリア 本", "獣医師国家試験 テキスト", "獣医学 入門 本", "獣医師 資格 教材"),
    "通訳・翻訳": ("通訳 翻訳 転職 本", "英検1級 TOEIC テキスト", "通訳 翻訳 入門 本", "英語 資格 教材"),
    "調理師": ("調理師 転職 本", "調理師免許 テキスト", "料理 入門 本", "調理師 資格 教材"),
}


def make_amazon_link(keywords):
    """Generate Amazon affiliate search link."""
    return f"https://www.amazon.co.jp/s?k={quote(keywords)}&tag={AMAZON_TAG}"


def make_rakuten_link(keywords):
    """Generate Rakuten affiliate search link."""
    rakuten_search = f"https://search.rakuten.co.jp/search/mall/{quote(keywords)}/"
    return f"https://hb.afl.rakuten.co.jp/ichiba/{RAKUTEN_AFF_ID}/?pc={quote(rakuten_search)}&link_type=hybrid_url"


def generate_affiliate_section(job_title):
    """Generate affiliate HTML sections for a job page."""
    kw = AFFILIATE_KEYWORDS.get(job_title, (f"{job_title} 転職 本", f"{job_title} 資格 テキスト", f"{job_title} 入門 本", f"{job_title} 資格 教材"))
    book_kw, study_kw, skill_book_kw, skill_study_kw = kw

    amazon_book = make_amazon_link(book_kw)
    rakuten_study = make_rakuten_link(study_kw)
    amazon_skill = make_amazon_link(skill_book_kw)
    rakuten_skill = make_rakuten_link(skill_study_kw)

    return f'''
    <div class="card affiliate-card">
      <h2>転職サービスおすすめ</h2>
      <p class="desc-text" style="margin-bottom:16px">{job_title}への転職・キャリアチェンジに役立つ書籍や教材をご紹介します。</p>
      <div class="affiliate-items">
        <div class="affiliate-item">
          <div class="affiliate-label">この職業に転職するためのおすすめ本</div>
          <p class="affiliate-desc">転職活動の進め方や業界知識を身につけるための厳選書籍をAmazonで探せます。</p>
          <div class="affiliate-buttons">
            <a href="{amazon_book}" class="affiliate-btn affiliate-btn-main" target="_blank" rel="noopener noreferrer nofollow">Amazonで書籍を探す</a>
          </div>
        </div>
        <div class="affiliate-item">
          <div class="affiliate-label">資格取得のための教材</div>
          <p class="affiliate-desc">資格試験の対策テキストや問題集を楽天市場で探せます。</p>
          <div class="affiliate-buttons">
            <a href="{rakuten_study}" class="affiliate-btn affiliate-btn-main" target="_blank" rel="noopener noreferrer nofollow">楽天市場で教材を探す</a>
          </div>
        </div>
      </div>
    </div>

    <div class="card affiliate-card">
      <h2>スキルアップにおすすめ</h2>
      <p class="desc-text" style="margin-bottom:16px">{job_title}としてキャリアアップするための学習教材をご紹介します。</p>
      <div class="affiliate-items">
        <div class="affiliate-item">
          <div class="affiliate-label">スキルアップのためのおすすめ本</div>
          <p class="affiliate-desc">実務で役立つスキルを身につけるための書籍をAmazonで探せます。</p>
          <div class="affiliate-buttons">
            <a href="{amazon_skill}" class="affiliate-btn affiliate-btn-main" target="_blank" rel="noopener noreferrer nofollow">Amazonで書籍を探す</a>
            <a href="{rakuten_skill}" class="affiliate-btn-sub" target="_blank" rel="noopener noreferrer nofollow">楽天市場で教材を探す &raquo;</a>
          </div>
        </div>
      </div>
    </div>
'''


def generate_job_page(job, category_name):
    """Generate a single job HTML page."""
    title = job["title"]
    avg = job["avg"]
    monthly = job["monthly"]
    bonus = job["bonus"]
    max_salary = max(max(job["ages"].values()), max(job["sizes"].values()))

    # Age bars
    age_bars = ""
    for age, sal in job["ages"].items():
        pct = int(sal / max_salary * 100)
        age_bars += f'''        <div class="bar-row">
          <div class="bar-label">{age}</div>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%"><span class="bar-value">{fmt(sal)}万円</span></div></div>
        </div>\n'''

    # Size bars
    size_bars = ""
    for size, sal in job["sizes"].items():
        pct = int(sal / max_salary * 100)
        size_bars += f'''        <div class="bar-row">
          <div class="bar-label" style="width:160px">{size}</div>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%"><span class="bar-value">{fmt(sal)}万円</span></div></div>
        </div>\n'''

    # Related jobs
    related_tags = ""
    for r in job.get("related", []):
        s = slug_for_title(r)
        if s:
            related_tags += f'        <a href="{s}.html" class="tag">{r}の年収</a>\n'

    # JSON-LD
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{title}の年収・給料情報 | 年収ナビ",
        "description": f"{title}の平均年収は{avg}万円です。月収や賞与、年代別・企業規模別の年収データを詳しく解説。",
        "url": f"{SITE_URL}/jobs/{job['slug']}.html",
        "isPartOf": {"@type": "WebSite", "name": "年収ナビ", "url": SITE_URL},
        "mainEntity": {
            "@type": "Occupation",
            "name": title,
            "estimatedSalary": {
                "@type": "MonetaryAmountDistribution",
                "name": "年収",
                "currency": "JPY",
                "median": avg * 10000,
                "unitText": "YEAR",
            },
        },
    }, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}の年収・給料｜平均年収{avg}万円【{YEAR}年最新】| 年収ナビ</title>
<meta name="description" content="{title}の平均年収は{avg}万円（{YEAR}年最新データ）。月収{monthly}万円、賞与{bonus}万円。年代別・企業規模別の年収も詳しく解説します。">
<meta name="keywords" content="{title} 年収,{title} 給料,{title} 平均年収,{title} 月収,{title} ボーナス">
<meta property="og:title" content="{title}の年収・給料｜平均年収{avg}万円【{YEAR}年最新】">
<meta property="og:description" content="{title}の平均年収は{avg}万円。年代別・企業規模別の年収データを詳しく解説。">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE_URL}/jobs/{job['slug']}.html">
<meta property="og:site_name" content="年収ナビ">
<link rel="canonical" href="{SITE_URL}/jobs/{job['slug']}.html">
<link rel="stylesheet" href="../css/style.css">
{ADSENSE}
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
  <header class="header">
    <div class="header-inner">
      <a href="../index.html" class="logo">年収ナビ<span>Salary Navigator</span></a>
      <nav class="nav">
        <a href="../index.html">トップ</a>
        <a href="../index.html#it">IT・エンジニア</a>
        <a href="../index.html#medical">医療</a>
        <a href="../index.html#finance">金融</a>
        <a href="../index.html#public">公務員</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <h1>{title}の年収・給料</h1>
    <p>{YEAR}年最新の年収データを徹底解説</p>
  </section>

  <main class="main">
    <div class="breadcrumb">
      <a href="../index.html">トップ</a> &gt; <a href="../index.html#{category_name}">{category_name}</a> &gt; {title}の年収
    </div>

    <div class="card">
      <div class="salary-hero">
        <div class="salary-big">{fmt(avg)}<small>万円</small></div>
        <p style="color:#64748b;font-size:.9rem;margin-top:4px">{title}の平均年収</p>
        <div class="salary-sub">
          <div class="salary-sub-item">
            <div class="label">月収（税込）</div>
            <div class="value">{fmt(monthly)}万円</div>
          </div>
          <div class="salary-sub-item">
            <div class="label">賞与（年間）</div>
            <div class="value">{fmt(bonus)}万円</div>
          </div>
          <div class="salary-sub-item">
            <div class="label">手取り月収（概算）</div>
            <div class="value">{fmt(int(monthly * 0.78))}万円</div>
          </div>
        </div>
      </div>
    </div>

    <div class="ad-space">広告</div>

    <div class="card">
      <h2>年代別の平均年収</h2>
      <div class="bar-chart">
{age_bars}      </div>
      <p class="desc-text" style="margin-top:14px">{title}の年収は経験年数とともに上昇し、{list(job["ages"].keys())[-1]}でピークを迎える傾向にあります。</p>
    </div>

    <div class="card">
      <h2>企業規模別の平均年収</h2>
      <div class="bar-chart">
{size_bars}      </div>
    </div>

    <div class="ad-space">広告</div>

    <div class="card">
      <h2>必要な資格・スキル</h2>
      <p class="desc-text">{job["qualifications"]}</p>
    </div>

    <div class="card">
      <h2>キャリアパス・将来性</h2>
      <p class="desc-text">{job["career"]}</p>
    </div>

    <div class="card">
      <h2>{title}の給与内訳</h2>
      <table class="info-table">
        <tr><th>平均年収</th><td>{fmt(avg)}万円</td></tr>
        <tr><th>平均月収（税込）</th><td>{fmt(monthly)}万円</td></tr>
        <tr><th>手取り月収（概算）</th><td>{fmt(int(monthly * 0.78))}万円</td></tr>
        <tr><th>平均賞与（年間）</th><td>{fmt(bonus)}万円</td></tr>
        <tr><th>時給換算（概算）</th><td>{fmt(int(avg * 10000 / 2080))}円</td></tr>
        <tr><th>生涯年収（概算）</th><td>{fmt(round(avg * 38 / 10000, 1))}億円</td></tr>
      </table>
    </div>

    <div class="ad-space">広告</div>

{generate_affiliate_section(title)}

    <div class="card">
      <h2>関連する職業の年収</h2>
      <div class="tag-list">
{related_tags}      </div>
    </div>
  </main>

  <footer class="footer">
    <p>&copy; {YEAR} 年収ナビ（Salary Navigator）- 日本の職業別年収データ</p>
    <p style="margin-top:8px"><a href="../index.html">トップページ</a></p>
  </footer>
</body>
</html>'''
    return html


def generate_index():
    """Generate the index page."""
    categories_html = ""
    for cat in CATEGORIES:
        categories_html += f'    <h3 class="category-title" id="{cat["slug"]}">{cat["name"]}</h3>\n'
        categories_html += '    <div class="job-grid">\n'
        for job in cat["jobs"]:
            categories_html += f'''      <a href="jobs/{job["slug"]}.html" class="job-card">
        <div class="job-name">{job["title"]}</div>
        <div class="job-salary">{fmt(job["avg"])}万円 <small>平均年収</small></div>
      </a>\n'''
        categories_html += '    </div>\n\n'

    total_jobs = sum(len(c["jobs"]) for c in CATEGORIES)

    # Index JSON-LD
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "年収ナビ",
        "url": SITE_URL,
        "description": f"日本の{total_jobs}職種の年収・給料データを網羅。年代別・企業規模別の年収情報を無料で確認できます。",
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/jobs/{{search_term}}.html",
            "query-input": "required name=search_term",
        },
    }, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>年収ナビ｜職業別の平均年収・給料データベース【{YEAR}年最新】</title>
<meta name="description" content="日本の{total_jobs}職種の平均年収・月収・賞与データを網羅。IT、医療、金融、公務員など各職業の年収を年代別・企業規模別に詳しく解説。{YEAR}年最新版。">
<meta name="keywords" content="年収,平均年収,給料,職業別年収,年収ランキング,月収,ボーナス">
<meta property="og:title" content="年収ナビ｜職業別の平均年収・給料データベース【{YEAR}年最新】">
<meta property="og:description" content="日本の{total_jobs}職種の平均年収データを網羅。年代別・企業規模別の年収情報を無料で確認。">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:site_name" content="年収ナビ">
<link rel="canonical" href="{SITE_URL}/">
<link rel="stylesheet" href="css/style.css">
{ADSENSE}
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
  <header class="header">
    <div class="header-inner">
      <a href="index.html" class="logo">年収ナビ<span>Salary Navigator</span></a>
      <nav class="nav">
        <a href="#it">IT・エンジニア</a>
        <a href="#medical">医療</a>
        <a href="#finance">金融</a>
        <a href="#public">公務員</a>
        <a href="#other">その他</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <h1>年収ナビ - 職業別年収データベース</h1>
    <p>{total_jobs}職種の年収・給料データを網羅（{YEAR}年最新版）</p>
  </section>

  <main class="main">
    <div class="card">
      <div class="stats-row">
        <div class="stat-box">
          <div class="stat-label">掲載職種数</div>
          <div class="stat-value">{total_jobs}職種</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">カテゴリ</div>
          <div class="stat-value">{len(CATEGORIES)}分野</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">最終更新</div>
          <div class="stat-value">{YEAR}年</div>
        </div>
      </div>
    </div>

    <div class="ad-space">広告</div>

{categories_html}
    <div class="ad-space">広告</div>

    <div class="card">
      <h2>年収ナビについて</h2>
      <div class="desc-text">
        <p>年収ナビは、日本の様々な職業の年収・給料情報をまとめたデータベースサイトです。厚生労働省の賃金構造基本統計調査や各種業界データをもとに、職業別の平均年収、月収、賞与、年代別・企業規模別の年収データを提供しています。</p>
        <p>就職・転職活動の参考や、キャリアプランニングにぜひご活用ください。</p>
      </div>
    </div>
  </main>

  <footer class="footer">
    <p>&copy; {YEAR} 年収ナビ（Salary Navigator）- 日本の職業別年収データ</p>
  </footer>
</body>
</html>'''
    return html


def generate_sitemap():
    """Generate sitemap.xml."""
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [f'  <url><loc>{SITE_URL}/</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>']
    for cat in CATEGORIES:
        for job in cat["jobs"]:
            urls.append(f'  <url><loc>{SITE_URL}/jobs/{job["slug"]}.html</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''


def generate_robots():
    """Generate robots.txt."""
    return f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    jobs_dir = os.path.join(base, "jobs")
    os.makedirs(jobs_dir, exist_ok=True)

    # Generate index
    with open(os.path.join(base, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_index())
    print("Generated: index.html")

    # Generate job pages
    count = 0
    for cat in CATEGORIES:
        for job in cat["jobs"]:
            path = os.path.join(jobs_dir, f'{job["slug"]}.html')
            with open(path, "w", encoding="utf-8") as f:
                f.write(generate_job_page(job, cat["slug"]))
            count += 1
            print(f"Generated: jobs/{job['slug']}.html ({job['title']})")

    # Generate sitemap
    with open(os.path.join(base, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(generate_sitemap())
    print("Generated: sitemap.xml")

    # Generate robots.txt
    with open(os.path.join(base, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(generate_robots())
    print("Generated: robots.txt")

    print(f"\nDone! Generated {count} job pages + index + sitemap + robots.txt")


if __name__ == "__main__":
    main()

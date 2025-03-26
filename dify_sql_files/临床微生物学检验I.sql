INSERT INTO application (
    seq,
    app_id,
    maxkb_id,
    name,
    icon,
    api_type,
    base_api,
    redirect_link,
    token,
    category,
    `desc`,
    prologue,
    enabled,
    visible,
    main_app
) VALUES (
    3000,
    uuid(),
    NULL,
    '临床微生物学检验I',
    11,
    'dify/chatflow',
    'http://10.119.14.166/v1/',
    NULL,
    'app-eM3Q8XPXogMGmY98EGLAikSR',
    'AI 课程/AI+课程/临床微生物学检验I/AI学伴',
    '授课教师：李敏',
    '临床微生物学检验是教育部规定的医学检验专业主干学科和必修课程，在医学检验人才培养中发挥主要作用。课程主要讲授微生物学检验基础理论及其检验基本技术；临床上重要的病原微生物的分类和命名、生物学特性、鉴定及鉴别要点和方法、对药物的敏感性与临床意义。
       通过本课程学习，学生能够初步掌握各类感染性疾病标本的微生物检验、结果报告与解释及抗微生物药物敏感试验和耐药性检查，有助于学生将理论知识运用于实际临床检验工作，为临床感染性疾病的诊断、治疗和预防发挥关键作用。',
    1,
    1,
    1
);
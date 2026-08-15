const { p, chapterLabel, blank, cleanText } = require('../helpers');
const { Paragraph, TextRun, AlignmentType } = require('docx');

function ref(text) {
  return new Paragraph({
    children: [new TextRun({ text: cleanText(text), font: 'Times New Roman', size: 24 })],
    alignment: AlignmentType.LEFT,
    spacing: { line: 300, after: 120 },
    indent: { left: 720, hanging: 720 },
  });
}

function references() {
  const b = [];

  b.push(chapterLabel('REFERENCES'));
  const refs = [
    'Ahmed, T., Ghosh, S., Bansal, C., Zimmermann, T., Zhang, X., & Rajmohan, S. (2023). Recommending root-cause and mitigation steps for cloud incidents using large language models. In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE) (pp. 1737-1749). IEEE. https://doi.org/10.1109/ICSE48619.2023.00149',
    'Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (Eds.). (2016). Site reliability engineering: How Google runs production systems. O\'Reilly Media.',
    'Brooke, J. (1996). SUS: A quick and dirty usability scale. In P. W. Jordan, B. Thomas, B. A. Weerdmeester, & I. L. McClelland (Eds.), Usability evaluation in industry (pp. 189-194). Taylor & Francis.',
    'Central Bank of Nigeria. (2024). Risk-based cybersecurity framework and guidelines for deposit money banks and payment service banks. https://www.cbn.gov.ng/Out/2024/BSD/CBN%20Risk-Based%20Cybersecurity%20Framework%20for%20DMBs%20and%20PSBs_2024.pdf',
    'Chen, Y., Xie, H., Ma, M., Kang, Y., Gao, X., Shi, L., Cao, Y., Gao, X., Fan, H., Wen, M., Zeng, J., Ghosh, S., Zhang, X., Zhang, C., Lin, Q., Rajmohan, S., Zhang, D., & Xu, T. (2024). Automatic root cause analysis via large language models for cloud incidents. In Proceedings of the Nineteenth European Conference on Computer Systems (pp. 674-688). Association for Computing Machinery. https://doi.org/10.1145/3627703.3629553',
    'Chen, Y., Shetty, M., Somashekar, G., Ma, M., Simmhan, Y., Mace, J., Bansal, C., Wang, R., & Rajmohan, S. (2025). AIOpsLab: A holistic framework to evaluate AI agents for enabling autonomous clouds. Proceedings of Machine Learning and Systems, 7. https://proceedings.mlsys.org/paper_files/paper/2025/hash/d1f9e4a9f109b6e8b75ed362736f22ec-Abstract-Conference.html',
    'Datadog. (n.d.). Knowledge sources for Bits Investigation. Retrieved July 30, 2026, from https://docs.datadoghq.com/bits_ai/bits_investigation/knowledge_sources/',
    'Federal Republic of Nigeria. (2023). Nigeria Data Protection Act, 2023. Nigeria Data Protection Commission. https://ndpc.gov.ng/download/nigeria-data-protection-act-2023',
    'Grafana Labs. (n.d.). Grafana Loki documentation. Retrieved July 30, 2026, from https://grafana.com/docs/loki/latest/',
    'Guo, H., Yang, J., Liu, J., Yang, L., Chai, L., Bai, J., Peng, J., Hu, X., Chen, C., Zhang, D., Shi, X., Zheng, T., Zheng, L., Zhang, B., Xu, K., & Li, Z. (2024). OWL: A large language model for IT operations. In The Twelfth International Conference on Learning Representations. https://openreview.net/forum?id=SZOQ9RKYJu',
    'He, P., Zhu, J., Zheng, Z., & Lyu, M. R. (2017). Drain: An online log parsing approach with fixed depth tree. In 2017 IEEE International Conference on Web Services (ICWS) (pp. 33-40). IEEE. https://doi.org/10.1109/ICWS.2017.13',
    'Hevner, A. R., March, S. T., Park, J., & Ram, S. (2004). Design science in information systems research. MIS Quarterly, 28(1), 75-105. https://doi.org/10.2307/25148625',
    'Hou, X., Zhao, Y., Liu, Y., Yang, Z., Wang, K., Li, L., Luo, X., Lo, D., Grundy, J., & Wang, H. (2024). Large language models for software engineering: A systematic literature review. ACM Transactions on Software Engineering and Methodology, 33(8), Article 220. https://doi.org/10.1145/3695988',
    'International Organization for Standardization. (2022). ISO/IEC 27001:2022 information security, cybersecurity and privacy protection: Information security management systems: Requirements. https://www.iso.org/standard/27001',
    'Jin, P., Zhang, S., Ma, M., Li, H., Kang, Y., Li, L., Liu, Y., Qiao, B., Zhang, C., Zhao, P., He, S., Sarro, F., Dang, Y., Rajmohan, S., Lin, Q., & Zhang, D. (2023). Assess and summarize: Improve outage understanding with large language models. In Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering (pp. 1657-1668). Association for Computing Machinery. https://doi.org/10.1145/3611643.3613891',
    'k8sgpt. (n.d.). Getting started guide. Retrieved July 30, 2026, from https://docs.k8sgpt.ai/getting-started/getting-started/',
    'LangChain. (n.d.). LangGraph overview. Retrieved July 30, 2026, from https://docs.langchain.com/oss/python/langgraph/overview',
    'Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Kuttler, H., Lewis, M., Yih, W., Rocktaschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459-9474. https://arxiv.org/abs/2005.11401',
    'National Institute of Standards and Technology. (2024). Artificial intelligence risk management framework: Generative artificial intelligence profile (NIST AI 600-1). U.S. Department of Commerce. https://doi.org/10.6028/NIST.AI.600-1',
    'New Relic. (n.d.). Meet New Relic AI, your observability assistant. Retrieved July 30, 2026, from https://docs.newrelic.com/docs/agentic-ai/new-relic-ai/',
    'OpenAPI Initiative. (2025). OpenAPI specification, version 3.1.2. https://spec.openapis.org/oas/v3.1.2.html',
    'OWASP Foundation. (2025). OWASP Top 10:2025. https://owasp.org/Top10/',
    'PagerDuty. (n.d.). PagerDuty AIOps. Retrieved July 30, 2026, from https://support.pagerduty.com/main/docs/aiops',
    'Prometheus Authors. (n.d.). Exposition formats. Retrieved July 30, 2026, from https://prometheus.io/docs/instrumenting/exposition_formats/',
    'Roy, D., Zhang, X., Bhave, R., Bansal, C., Las-Casas, P. H. B., Fonseca, R., & Rajmohan, S. (2024). Exploring LLM-based agents for root cause analysis. In Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering (pp. 208-219). Association for Computing Machinery. https://doi.org/10.1145/3663529.3663841',
    'Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. (2023). Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36, 8634-8652. https://doi.org/10.52202/075280-0377',
    'Xu, J., Zhang, Q., Zhong, Z., He, S., Zhang, C., Lin, Q., Pei, D., He, P., Zhang, D., & Zhang, Q. (2025). OpenRCA: Can large language models locate the root cause of software failures? In International Conference on Learning Representations. https://proceedings.iclr.cc/paper_files/paper/2025/hash/d29b8d53678015079e1d245c023e49d2-Abstract-Conference.html',
    'Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). ReAct: Synergizing reasoning and acting in language models. In The Eleventh International Conference on Learning Representations. https://openreview.net/forum?id=WE_vluYUL-X',
    'Yuan, P., Tang, L., Liu, Y., Kobayashi, Y., Sato, M., & Chen, H. (2025). Incident diagnosing and reporting system based on retrieval augmented large language model. Proceedings of the AAAI Conference on Artificial Intelligence, 39(28), 29721-29723. https://doi.org/10.1609/aaai.v39i28.35379',
  ];

  for (const entry of refs) b.push(ref(entry));
  return b;
}

module.exports = { references };

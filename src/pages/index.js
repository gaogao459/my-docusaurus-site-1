import React from 'react';
import Layout from '@theme/Layout';
import styles from './index.module.css';

export default function Home() {
  return (
    <Layout
      title="Make.com 网站复刻"
      description="Make 是一个可视化平台，任何人都可以通过它设计、构建和自动化任何事物">
      
      {/* Header Section */}
      <header className={styles.header}>
        <nav className={`${styles.container} ${styles.nav}`}>
          {/* Logo */}
          <div className={styles.logo}>Make.</div>
          {/* Navigation Links */}
          <ul className={styles.navLinks}>
            <li><a href="#" className={styles.navLink}>解决方案</a></li>
            <li><a href="#" className={styles.navLink}>平台</a></li>
            <li><a href="#" className={styles.navLink}>定价</a></li>
            <li><a href="#" className={styles.navLink}>资源</a></li>
            <li><a href="#" className={styles.navLink}>公司</a></li>
          </ul>
          {/* Buttons */}
          <div className={styles.navButtons}>
            <button className={styles.loginButton}>登录</button>
            <button className={styles.ctaButton}>免费开始</button>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className={styles.hero}>
        <div className={`${styles.container} ${styles.heroContent}`}>
          {/* Left Content */}
          <div className={styles.heroLeft}>
            <h1 className={styles.heroTitle}>
              <span className={styles.block}>您能看到并</span>
              <span className={styles.block}>理解的自动化。</span>
            </h1>
            <p className={styles.heroSubtitle}>
              Make 是一个可视化平台，任何人都可以通过它设计、构建和自动化任何事物——从任务和工作流到应用程序和系统。
            </p>
            <div className={styles.heroButtons}>
              <button className={styles.primaryButton}>免费开始</button>
              <button className={styles.secondaryButton}>预约演示</button>
            </div>
          </div>
          {/* Right Image/Graphic Placeholder */}
          <div className={styles.heroRight}>
            <img 
              src="/img/hero-automation.png" 
              alt="AI 自动化图形" 
              className={styles.heroImage}
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          </div>
        </div>
      </section>

      {/* Visualize a core production future with Make + AI Section */}
      <section className={`${styles.section} ${styles.sectionGray}`}>
        <div className={styles.container}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>使用 Make + AI 展望核心生产未来</h2>
            <p className={styles.sectionSubtitle}>
              Make 是一个可视化平台，任何人都可以通过它设计、构建和自动化任何事物——从任务和工作流到应用程序和系统。
            </p>
          </div>
          <div className={`${styles.grid} ${styles.gridCols1} ${styles.mdGridCols3}`}>
            {/* Card 1 */}
            <div className={styles.card}>
              <div className={`${styles.cardIcon} ${styles.cardIconBlue}`}>
                <span>💡</span>
              </div>
              <h3 className={styles.cardTitle}>可视化工作流构建器</h3>
              <p className={styles.cardText}>
                拖放即可创建强大的集成和自动化。
              </p>
            </div>
            {/* Card 2 */}
            <div className={styles.card}>
              <div className={`${styles.cardIcon} ${styles.cardIconPurple}`}>
                <span>🚀</span>
              </div>
              <h3 className={styles.cardTitle}>AI 驱动的自动化</h3>
              <p className={styles.cardText}>
                利用 AI 增强您的工作流并做出更明智的决策。
              </p>
            </div>
            {/* Card 3 */}
            <div className={styles.card}>
              <div className={`${styles.cardIcon} ${styles.cardIconGreen}`}>
                <span>🔗</span>
              </div>
              <h3 className={styles.cardTitle}>连接一切</h3>
              <p className={styles.cardText}>
                与数千个应用程序和服务集成。
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Accelerate innovation across your business Section */}
      <section className={`${styles.section} ${styles.sectionWhite}`}>
        <div className={styles.container}>
          <div className={`${styles.flex} ${styles.flexCol} ${styles.lgFlexRow} ${styles.itemsCenter} ${styles.gap12}`}>
            {/* Left Content */}
            <div className={`${styles.textCenter} ${styles.lgTextLeft} ${styles.lgWHalf}`}>
              <h2 className={styles.sectionTitle}>加速您业务的创新</h2>
              <p className={`${styles.sectionSubtitle} ${styles.mb8}`}>
                Make 赋能团队无限构建和自动化，促进创新和效率。
              </p>
              <ul className={styles.featureList}>
                <li className={styles.featureItem}>
                  <span className={styles.featureIcon}>✔</span>
                  <p className={styles.featureText}>通过可视化工作流简化操作。</p>
                </li>
                <li className={styles.featureItem}>
                  <span className={styles.featureIcon}>✔</span>
                  <p className={styles.featureText}>自动化重复性任务以节省时间和资源。</p>
                </li>
                <li className={styles.featureItem}>
                  <span className={styles.featureIcon}>✔</span>
                  <p className={styles.featureText}>连接不同的系统以实现无缝数据流。</p>
                </li>
                <li className={styles.featureItem}>
                  <span className={styles.featureIcon}>✔</span>
                  <p className={styles.featureText}>赋能非技术用户构建解决方案。</p>
                </li>
              </ul>
            </div>
            {/* Right Image */}
            <div className={`${styles.justifyCenter} ${styles.lgJustifyEnd} ${styles.lgWHalf}`}>
              <img 
                src="/img/business-automation.png" 
                alt="业务自动化桌面" 
                className={styles.image}
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
          </div>

          {/* Icons below the section */}
          <div className={`${styles.grid} ${styles.gridCols2} ${styles.mdGridCols4} ${styles.lgGridCols6} ${styles.mt16} ${styles.itemsCenter} ${styles.justifyCenter}`}>
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
              <div className={`${styles.smallIcon} ${styles.cardIconGray}`}>
                <span>⚙️</span>
              </div>
              <p className={styles.smallIconText}>运营</p>
            </div>
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
              <div className={`${styles.smallIcon} ${styles.cardIconGray}`}>
                <span>📊</span>
              </div>
              <p className={styles.smallIconText}>营销</p>
            </div>
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
              <div className={`${styles.smallIcon} ${styles.cardIconGray}`}>
                <span>💰</span>
              </div>
              <p className={styles.smallIconText}>财务</p>
            </div>
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
              <div className={`${styles.smallIcon} ${styles.cardIconGray}`}>
                <span>📞</span>
              </div>
              <p className={styles.smallIconText}>销售</p>
            </div>
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
              <div className={`${styles.smallIcon} ${styles.cardIconGray}`}>
                <span>👩‍💻</span>
              </div>
              <p className={styles.smallIconText}>IT</p>
            </div>
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
              <div className={`${styles.smallIcon} ${styles.cardIconGray}`}>
                <span>🤝</span>
              </div>
              <p className={styles.smallIconText}>人力资源</p>
            </div>
          </div>
        </div>
      </section>

      {/* Unleash the full potential of automation with AI Section */}
      <section className={`${styles.section} ${styles.sectionGradient}`}>
        <div className={styles.container}>
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle}>释放 AI 自动化的全部潜力</h2>
            <p className={styles.sectionSubtitle}>
              探索 Make 的 AI 功能如何彻底改变您的工作流并带来前所未有的效率。
            </p>
          </div>
          <div className={`${styles.grid} ${styles.gridCols1} ${styles.mdGridCols3}`}>
            {/* Card 1 */}
            <div className={`${styles.card} ${styles.cardGradient}`}>
              <h3 className={styles.cardTitle}>AI 驱动的数据处理</h3>
              <p className={`${styles.cardText} ${styles.mb6}`}>
                利用智能 AI 自动化数据提取、转换和加载。
              </p>
              <button className={styles.buttonWhite}>了解更多</button>
            </div>
            {/* Card 2 */}
            <div className={`${styles.card} ${styles.cardGradient}`}>
              <h3 className={styles.cardTitle}>智能决策</h3>
              <p className={`${styles.cardText} ${styles.mb6}`}>
                利用 AI 在您的自动化工作流中做出实时决策。
              </p>
              <button className={styles.buttonWhite}>了解更多</button>
            </div>
            {/* Card 3 */}
            <div className={`${styles.card} ${styles.cardGradient}`}>
              <h3 className={styles.cardTitle}>内容生成与摘要</h3>
              <p className={`${styles.cardText} ${styles.mb6}`}>
                通过 AI 自动化内容创建和摘要任务。
              </p>
              <button className={styles.buttonWhite}>了解更多</button>
            </div>
          </div>
        </div>
      </section>

      {/* Automation for Every Team Section */}
      <section className={`${styles.section} ${styles.sectionGray}`}>
        <div className={styles.container}>
          <div className={`${styles.flex} ${styles.flexCol} ${styles.lgFlexRow} ${styles.itemsCenter} ${styles.gap12}`}>
            {/* Left Content */}
            <div className={`${styles.textCenter} ${styles.lgTextLeft} ${styles.lgWHalf}`}>
              <h2 className={styles.sectionTitle}>为每个团队提供自动化</h2>
              <p className={`${styles.sectionSubtitle} ${styles.mb8}`}>
                无论您身处营销、销售、IT 还是人力资源，Make 都提供量身定制的解决方案，以自动化您团队的独特工作流。
              </p>
              <button className={styles.buttonPurple}>探索解决方案</button>
            </div>
            {/* Right Image/Graphic Placeholder */}
            <div className={`${styles.justifyCenter} ${styles.lgJustifyEnd} ${styles.lgWHalf}`}>
              <img 
                src="/img/team-automation.png" 
                alt="团队自动化图形" 
                className={styles.imageLarge}
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Unleash the full potential of AI section */}
      <section className={`${styles.section} ${styles.sectionWhite}`}>
        <div className={styles.container}>
          <div className={`${styles.flex} ${styles.flexCol} ${styles.lgFlexRow} ${styles.itemsCenter} ${styles.gap12}`}>
            {/* Left Image/Graphic Placeholder */}
            <div className={`${styles.justifyCenter} ${styles.lgJustifyStart} ${styles.lgOrder1} ${styles.lgWHalf}`}>
              <img 
                src="/img/ai-interconnected.png" 
                alt="互联的 AI 图标" 
                className={styles.imageLarge}
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
            {/* Right Content */}
            <div className={`${styles.textCenter} ${styles.lgTextLeft} ${styles.order1} ${styles.lgOrder2} ${styles.lgWHalf}`}>
              <h2 className={styles.sectionTitle}>释放 AI 的全部潜力</h2>
              <p className={`${styles.sectionSubtitle} ${styles.mb8}`}>
                将 AI 集成到您的核心业务流程中，以大规模推动创新和效率。
              </p>
              <button className={styles.buttonPurple}>了解更多</button>
            </div>
          </div>
        </div>
      </section>

      {/* Security and Compliance Section */}
      <section className={`${styles.section} ${styles.sectionGray}`}>
        <div className={styles.container}>
          <div className={`${styles.grid} ${styles.gridCols1} ${styles.lgGridCols2} ${styles.gap12} ${styles.itemsCenter}`}>
            {/* Left Content (3 columns of icons/text) */}
            <div className={`${styles.grid} ${styles.gridCols1} ${styles.mdGridCols3} ${styles.gap8}`}>
              {/* Security Feature 1 */}
              <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
                <div className={`${styles.cardIcon} ${styles.cardIconBlue}`}>
                  <span>🔒</span>
                </div>
                <h3 className={styles.cardTitle}>数据加密</h3>
                <p className={styles.cardText}>您的数据通过行业领先的加密技术得到保护。</p>
              </div>
              {/* Security Feature 2 */}
              <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
                <div className={`${styles.cardIcon} ${styles.cardIconRed}`}>
                  <span>🛡️</span>
                </div>
                <h3 className={styles.cardTitle}>合规标准</h3>
                <p className={styles.cardText}>遵守全球合规法规。</p>
              </div>
              {/* Security Feature 3 */}
              <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.textCenter}`}>
                <div className={`${styles.cardIcon} ${styles.cardIconGreen}`}>
                  <span>✅</span>
                </div>
                <h3 className={styles.cardTitle}>定期审计</h3>
                <p className={styles.cardText}>持续的安全审计和更新。</p>
              </div>
            </div>
            {/* Right Content (Text and button) */}
            <div className={`${styles.textCenter} ${styles.lgTextLeft}`}>
              <h2 className={styles.sectionTitle}>值得信赖的安全与合规</h2>
              <p className={`${styles.sectionSubtitle} ${styles.mb8}`}>
                Make 以安全为核心构建，确保您的数据和操作始终受到保护。
              </p>
              <button className={styles.buttonPurple}>了解更多</button>
            </div>
          </div>
        </div>
      </section>

      {/* Customer Logos Section */}
      <section className={`${styles.section} ${styles.sectionWhite}`}>
        <div className={styles.container}>
          <div className={styles.textCenter}>
            <h2 className={`${styles.sectionTitle} ${styles.mb12}`}>加入数千家通过 Make 实现转型的企业</h2>
            <div className={styles.customerLogos}>
              {/* Placeholder Logos */}
              <img src="/img/customer-logo-1.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-2.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-3.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-4.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-5.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-6.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-7.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-8.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-9.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
              <img src="/img/customer-logo-10.png" alt="客户标志" className={styles.customerLogo} onError={(e) => e.target.style.display = 'none'} />
            </div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className={styles.footer}>
        <div className={styles.container}>
          {/* Top part of footer */}
          <div className={styles.footerTop}>
            <h2 className={styles.footerTitle}>充分发挥您的业务潜力</h2>
            <div className={styles.footerForm}>
              <input 
                type="email" 
                placeholder="输入您的邮箱" 
                className={styles.footerInput}
              />
              <button className={styles.buttonGreen}>免费开始</button>
            </div>
          </div>

          <hr className={styles.footerDivider} />

          {/* Footer Navigation Links */}
          <div className={styles.footerNav}>
            <div className={styles.footerColumn}>
              <h4 className={styles.footerColumnTitle}>解决方案</h4>
              <ul className={styles.footerLinks}>
                <li><a href="#" className={styles.footerLink}>面向营销</a></li>
                <li><a href="#" className={styles.footerLink}>面向销售</a></li>
                <li><a href="#" className={styles.footerLink}>面向 IT</a></li>
                <li><a href="#" className={styles.footerLink}>面向人力资源</a></li>
                <li><a href="#" className={styles.footerLink}>面向财务</a></li>
              </ul>
            </div>
            <div className={styles.footerColumn}>
              <h4 className={styles.footerColumnTitle}>公司</h4>
              <ul className={styles.footerLinks}>
                <li><a href="#" className={styles.footerLink}>关于我们</a></li>
                <li><a href="#" className={styles.footerLink}>职业</a></li>
                <li><a href="#" className={styles.footerLink}>新闻</a></li>
                <li><a href="#" className={styles.footerLink}>合作伙伴</a></li>
              </ul>
            </div>
            <div className={styles.footerColumn}>
              <h4 className={styles.footerColumnTitle}>资源</h4>
              <ul className={styles.footerLinks}>
                <li><a href="#" className={styles.footerLink}>博客</a></li>
                <li><a href="#" className={styles.footerLink}>案例研究</a></li>
                <li><a href="#" className={styles.footerLink}>帮助中心</a></li>
                <li><a href="#" className={styles.footerLink}>社区</a></li>
              </ul>
            </div>
            <div className={styles.footerColumn}>
              <h4 className={styles.footerColumnTitle}>法律</h4>
              <ul className={styles.footerLinks}>
                <li><a href="#" className={styles.footerLink}>服务条款</a></li>
                <li><a href="#" className={styles.footerLink}>隐私政策</a></li>
                <li><a href="#" className={styles.footerLink}>Cookie 政策</a></li>
              </ul>
            </div>
            {/* Social media icons and language selector */}
            <div className={`${styles.flex} ${styles.flexCol} ${styles.itemsCenter} ${styles.mdItemsStart}`}>
              <h4 className={styles.footerColumnTitle}>关注我们</h4>
              <div className={styles.socialLinks}>
                <a href="#" className={styles.socialLink}>F</a>
                <a href="#" className={styles.socialLink}>T</a>
                <a href="#" className={styles.socialLink}>L</a>
              </div>
              <select className={styles.languageSelect}>
                <option>English</option>
                <option>中文</option>
              </select>
            </div>
          </div>

          <div className={styles.footerCopyright}>
            © 2025 Make. 版权所有。
          </div>
        </div>
      </footer>
    </Layout>
  );
}

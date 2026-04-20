async function loadContent() {
    try {
        const sectionsRes = await fetch('/api/sections');
        const sections = await sectionsRes.json();

        sections.forEach(section => {
            const element = document.getElementById(`${section.key}`);
            if (element) {
                if (section.key === 'hero_subtitle') {
                    element.innerHTML = section.content.split(' | ').join(' <span class="separator">|</span> ');
                } else if (section.key === 'technical_skills') {
                    element.innerHTML = section.content.split(', ').map(skill => `<span>${escapeHtml(skill)}</span>`).join('');
                } else if (section.key === 'profile_picture_url') {
                    const heroProfilePic = document.getElementById('hero-profile-picture');
                    if (heroProfilePic) heroProfilePic.src = section.content;
                } else if (['education_content', 'experience_content', 'leadership_content'].includes(section.key)) {
                    element.innerHTML = section.content.split(' | ').map(item => `<div class="content-item">${escapeHtml(item)}</div>`).join('');
                } else if (section.key === 'hobbies_content') {
                    element.innerHTML = section.content.split(', ').map(hobby => `<span class="hobby-tag">${escapeHtml(hobby)}</span>`).join('');
                } else if (section.key === 'hero_achievements') {
                    element.innerHTML = section.content.split(', ').map(ach => `<span><i class="fas fa-check-circle"></i> ${escapeHtml(ach)}</span>`).join('');
                } else {
                    element.textContent = section.content;
                }
            }

            if (section.key === 'resume_url') {
                const resumeHero = document.getElementById('resume-hero');
                const resumeContact = document.getElementById('resume-contact');
                const url = section.content.startsWith('/') ? section.content : '/' + section.content;
                if (resumeHero) resumeHero.href = url;
                if (resumeContact) resumeContact.href = url;
            }
        });

        const projectsRes = await fetch('/api/projects');
        const projects = await projectsRes.json();

        const projectsGrid = document.getElementById('projects-grid');
        if (projects.length) {
            projectsGrid.innerHTML = projects.map(project => `
                <div class="project-card">
                    <div class="content">
                        <h3>${escapeHtml(project.title)}</h3>
                        <p>${escapeHtml(project.description)}</p>
                        <div class="project-tech">
                            ${project.technologies.map(tech => `<span>${escapeHtml(tech)}</span>`).join('')}
                        </div>
                        <div class="project-links">
                            ${project.github_link ? `<a href="${project.github_link}" target="_blank"><i class="fab fa-github"></i> Code</a>` : ''}
                            ${project.demo_link ? `<a href="${project.demo_link}" target="_blank"><i class="fas fa-external-link-alt"></i> Demo</a>` : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        const certsRes = await fetch('/api/certifications');
        const certs = await certsRes.json();

        const certsGrid = document.getElementById('certs-grid');
        if (certs.length) {
            certsGrid.innerHTML = certs.map(cert => `
                <div class="cert-card">
                    <div class="cert-badge"><i class="fas fa-certificate"></i> Verified</div>
                    <h3>${escapeHtml(cert.name)}</h3>
                    <div class="issuer">${escapeHtml(cert.issuer)}</div>
                    <div class="date"><i class="far fa-calendar-alt"></i> ${escapeHtml(cert.date_earned)}</div>
                    ${cert.credential_id ? `<div class="credential-id"><i class="fas fa-id-card"></i> ID: ${escapeHtml(cert.credential_id)}</div>` : ''}
                    <div class="cert-skills">
                        ${cert.skills.map(skill => `<span>${escapeHtml(skill)}</span>`).join('')}
                    </div>
                    ${cert.pdf_filename ? `
                        <div class="cert-actions">
                            <button onclick="viewCertificate('${cert.pdf_filename}')" class="btn-view">
                                <i class="fas fa-eye"></i> View Certificate
                            </button>
                            <a href="/static/certificates/${cert.pdf_filename}" download class="btn-pdf">
                                <i class="fas fa-download"></i> Download PDF
                            </a>
                        </div>
                    ` : '<div class="cert-actions"><span>No digital certificate available</span></div>'}
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading content:', error);
    }
}

function viewCertificate(filename) {
    const modal = document.getElementById('certModal');
    const pdfViewer = document.getElementById('pdfViewer');
    const imageViewer = document.getElementById('imageViewer');
    const downloadLink = document.getElementById('modalDownload');
    const extension = filename.split('.').pop().toLowerCase();
    const filePath = `/static/certificates/${filename}`;

    downloadLink.href = filePath;

    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
        imageViewer.src = filePath;
        imageViewer.style.display = 'block';
        pdfViewer.style.display = 'none';
        pdfViewer.src = '';
    } else {
        pdfViewer.src = filePath;
        pdfViewer.style.display = 'block';
        imageViewer.style.display = 'none';
        imageViewer.src = '';
    }

    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

document.querySelector('.close-modal')?.addEventListener('click', () => {
    closeModal();
});

function closeModal() {
    const modal = document.getElementById('certModal');
    const pdfViewer = document.getElementById('pdfViewer');
    const imageViewer = document.getElementById('imageViewer');
    modal.style.display = 'none';
    pdfViewer.src = '';
    imageViewer.src = '';
    document.body.style.overflow = 'auto';
}

window.onclick = function (event) {
    const modal = document.getElementById('certModal');
    if (event.target === modal) {
        closeModal();
    }
};

document.getElementById('contact-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const formData = {
        name: form.name.value,
        email: form.email.value,
        message: form.message.value
    };

    const messageDiv = document.getElementById('form-message');
    messageDiv.innerHTML = '<div style="color: #2563eb;"><i class="fas fa-spinner fa-spin"></i> Sending...</div>';

    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        const data = await response.json();

        if (data.success) {
            messageDiv.innerHTML = '<div style="color: #10b981;"><i class="fas fa-check-circle"></i> ✓ Message sent successfully!</div>';
            form.reset();
            setTimeout(() => messageDiv.innerHTML = '', 3000);
        } else {
            messageDiv.innerHTML = '<div style="color: #ef4444;"><i class="fas fa-exclamation-circle"></i> Error sending message.</div>';
        }
    } catch (error) {
        messageDiv.innerHTML = '<div style="color: #ef4444;"><i class="fas fa-wifi"></i> Network error. Please try again.</div>';
    }
});

document.querySelector('.menu-toggle')?.addEventListener('click', () => {
    document.querySelector('.nav-links')?.classList.toggle('active');
});

// Close mobile menu when a link is clicked
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelector('.nav-links')?.classList.remove('active');
    });
});

function switchScreen(sectionId) {
    const sections = ['home', 'about', 'experience', 'leadership', 'projects', 'certifications', 'contact'];
    const targetId = sectionId.replace('#', '');

    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            if (id === targetId) {
                section.style.display = id === 'home' ? 'flex' : 'block';
                setTimeout(() => section.style.opacity = '1', 10);
            } else {
                section.style.display = 'none';
                section.style.opacity = '0';
            }
        }
    });

    // Update active nav link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === `#${targetId}`);
    });

    window.scrollTo(0, 0);
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (!href || href === '#' || !href.startsWith('#')) return;

        e.preventDefault();
        switchScreen(href);

        const navLinks = document.querySelector('.nav-links');
        if (navLinks && navLinks.style.display === 'flex') {
            navLinks.style.display = 'none';
        }
    });
});

// Initialize with home screen
document.addEventListener('DOMContentLoaded', () => {
    loadContent();
    switchScreen('home');
});

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
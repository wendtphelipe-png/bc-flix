-- 1. ADICIONAR NOVAS COLUNAS À TABELA DE EVENTOS
ALTER TABLE eventos_bc 
ADD COLUMN IF NOT EXISTS data_inicio DATE,
ADD COLUMN IF NOT EXISTS data_fim DATE,
ADD COLUMN IF NOT EXISTS usar_data_fim BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS horario_inicio TIME,
ADD COLUMN IF NOT EXISTS horario_fim TIME,
ADD COLUMN IF NOT EXISTS usar_horario_fim BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS endereco TEXT,
ADD COLUMN IF NOT EXISTS ao_vivo BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS link_ao_vivo TEXT;

-- 2. CRIAR BUCKET DE IMAGENS (Se não possuir o bucket 'event_images')
-- Nota: Caso este comando falhe, você pode criar manualmente no painel Storage com o nome 'event_images' (Público)
INSERT INTO storage.buckets (id, name, public) 
VALUES ('event_images', 'event_images', true)
ON CONFLICT (id) DO NOTHING;

-- 3. POLÍTICAS DE ACESSO AO STORAGE (Permitir que usuários autenticados façam upload)
-- Substitua 'authenticated' pela role desejada se necessário, mas geralmente admins são authenticated.
CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'event_images');
CREATE POLICY "Admin Delete" ON storage.objects FOR DELETE USING (bucket_id = 'event_images');

-- 4. CRIAR TABELA DE CHECK-INS REALIZADOS (Se não existir)
CREATE TABLE IF NOT EXISTS checkins_realizados (
    id BIGSERIAL PRIMARY KEY,
    evento_id TEXT REFERENCES eventos_bc(id),
    medico_nome TEXT,
    nomeAnuncio TEXT,
    email TEXT,
    crm TEXT,
    whatsapp TEXT,
    bio TEXT,
    data_checkin TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS e permitir inserts públicos (ou conforme política desejada)
ALTER TABLE checkins_realizados ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable insert for all" ON checkins_realizados FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable select for admin" ON checkins_realizados FOR SELECT USING (true);

interface Config {
  apiUrl: string;
  apiVersion: string;
  isDev: boolean;
  uploadMaxSize: number;
  features: {
    darkMode: boolean;
    filePreview: boolean;
  };
  minio: {
    endpoint: string;
    bucket: string;
  };
}

export const config: Config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  apiVersion: process.env.NEXT_PUBLIC_API_VERSION || 'v1',
  isDev: process.env.NEXT_PUBLIC_DEV_MODE === 'true',
  uploadMaxSize: parseInt(process.env.NEXT_PUBLIC_UPLOAD_MAX_SIZE || '100000000', 10),
  features: {
    darkMode: process.env.NEXT_PUBLIC_ENABLE_DARK_MODE === 'true',
    filePreview: process.env.NEXT_PUBLIC_ENABLE_FILE_PREVIEW === 'true',
  },
  minio: {
    endpoint: process.env.NEXT_PUBLIC_MINIO_ENDPOINT || 'http://localhost:9000',
    bucket: process.env.NEXT_PUBLIC_MINIO_BUCKET || 'files',
  },
}

export function getApiUrl(path: string): string {
  return `${config.apiUrl}/api/${config.apiVersion}${path}`
}

export function getMinioUrl(objectPath: string): string {
  return `${config.minio.endpoint}/${config.minio.bucket}/${objectPath}`
}

export function formatBytes(bytes: number, decimals = 2): string {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const dm = decimals < 0 ? 0 : decimals
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']

  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}

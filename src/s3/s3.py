"""
Provide abstraction for S3-compatible object storage (e.g., MinIO).

- Upload, download, delete, list objects.
- Wrap logic into classes (e.g., S3Storage).
- Useful for file attachments, media uploads, etc.

Recommended: isolate storage logic from business logic.
"""
from minio import Minio
from pathlib import Path
from typing import BinaryIO

from src.config import cfg
from src.core.logger import get_logger

logger = get_logger()


class S3:
    def __init__(self) -> None:
        self.client = Minio(
            cfg.s3.aws_host,
            access_key=cfg.s3.aws_access_key,
            secret_key=cfg.s3.aws_secret_access_key,
            secure=False if "localhost" in cfg.s3.aws_host else True,
        )

    def ensure_bucket(self, bucket: str) -> None:
        """Create bucket if not exists."""
        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)
            logger.info(f"Created bucket: {bucket}")

    def upload(
        self,
        bucket: str,
        object_name: str,
        data: BinaryIO,
        length: int,
        content_type: str = "application/octet-stream",
    ) -> str:
        """Upload object to bucket."""
        self.ensure_bucket(bucket)
        self.client.put_object(
            bucket,
            object_name,
            data,
            length,
            content_type=content_type,
        )
        logger.info(f"Uploaded to {bucket}/{object_name}")
        return f"{bucket}/{object_name}"

    def upload_file(self, bucket: str, file_path: Path) -> str:
        """Upload local file to bucket."""
        with file_path.open("rb") as f:
            return self.upload(
                bucket,
                object_name=file_path.name,
                data=f,
                length=file_path.stat().st_size,
                content_type="application/octet-stream",
            )

    def download(self, bucket: str, object_name: str) -> bytes:
        """Download object as bytes."""
        response = self.client.get_object(bucket, object_name)
        data = response.read()
        response.close()
        response.release_conn()
        logger.info(f"Downloaded {bucket}/{object_name}")
        return data

    def delete(self, bucket: str, object_name: str) -> None:
        """Delete object from bucket."""
        self.client.remove_object(bucket, object_name)
        logger.info(f"Deleted {bucket}/{object_name}")

    def list_objects(self, bucket: str, prefix: str = "") -> list[str]:
        """List all object names in a bucket."""
        objects = self.client.list_objects(bucket, prefix=prefix, recursive=True)
        return [obj.object_name for obj in objects]
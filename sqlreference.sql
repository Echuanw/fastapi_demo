class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "jwt_demo"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    is_email_verified = Column(Boolean, nullable=False, default=False)
    last_login_at = Column(TIMESTAMP, nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    profile = relationship("UserProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_profiles_user_id"), {"schema": "jwt_demo"})

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("jwt_demo.users.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    avatar_url = Column(String(255))
    locale = Column(String(10))
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    user = relationship("User", back_populates="profile")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = {"schema": "jwt_demo"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("jwt_demo.users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), nullable=False)                                  # refresh_token 的哈希值
    jti = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=True)            # refresh_token 的 uuid
    expires_at = Column(TIMESTAMP, nullable=False)
    is_revoked = Column(Boolean, nullable=False, default=False)
    created_ip = Column(String(255), nullable=False)
    user_agent = Column(Text)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    user = relationship("User", back_populates="refresh_tokens")
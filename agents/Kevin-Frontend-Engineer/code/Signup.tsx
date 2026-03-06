import React, { useState } from 'react';
import Card from '../components/Card';
import PasswordStrength from '../components/PasswordStrength';
import Toast from '../components/Toast';

interface FieldErrors {
  email?: string;
  password?: string;
  passwordConfirm?: string;
}

export const Signup: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [errors, setErrors] = useState<FieldErrors>({});
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type?: 'success' | 'error' } | null>(null);

  const validate = (): boolean => {
    const e: FieldErrors = {};
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) e.email = '유효한 이메일을 입력하세요.';
    if (password.length < 8) e.password = '비밀번호는 8자 이상이어야 합니다.';
    if (password !== passwordConfirm) e.passwordConfirm = '비밀번호가 일치하지 않습니다.';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    setErrors({});

    try {
      // Mock API call: stubbed response
      await new Promise((res) => setTimeout(res, 600));
      setToast({ message: '회원가입이 완료되었습니다.', type: 'success' });
    } catch (err) {
      setToast({ message: '네트워크 오류가 발생했습니다.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <Card className="max-w-md w-full">
        <h1 className="text-2xl font-semibold mb-4">회원가입</h1>
        <form onSubmit={onSubmit} noValidate>
          <label className="block text-sm font-medium text-gray-700">이메일</label>
          <input
            className="mt-1 block w-full border border-gray-200 rounded px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? 'email-error' : undefined}
          />
          {errors.email && <div id="email-error" className="text-sm text-red-600 mt-1">{errors.email}</div>}

          <label className="block text-sm font-medium text-gray-700 mt-4">비밀번호</label>
          <input
            className="mt-1 block w-full border border-gray-200 rounded px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            aria-invalid={!!errors.password}
            aria-describedby={errors.password ? 'password-error' : undefined}
          />
          {errors.password && <div id="password-error" className="text-sm text-red-600 mt-1">{errors.password}</div>}

          <PasswordStrength password={password} />

          <label className="block text-sm font-medium text-gray-700 mt-4">비밀번호 확인</label>
          <input
            className="mt-1 block w-full border border-gray-200 rounded px-3 py-2"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            type="password"
            aria-invalid={!!errors.passwordConfirm}
            aria-describedby={errors.passwordConfirm ? 'passwordConfirm-error' : undefined}
          />
          {errors.passwordConfirm && <div id="passwordConfirm-error" className="text-sm text-red-600 mt-1">{errors.passwordConfirm}</div>}

          <button
            type="submit"
            className="mt-6 w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
            disabled={loading}
          >
            {loading ? '처리중...' : '계정 만들기'}
          </button>
        </form>
      </Card>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
};

export default Signup;

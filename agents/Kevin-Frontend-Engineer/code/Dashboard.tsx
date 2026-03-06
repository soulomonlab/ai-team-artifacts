import React from 'react';
import Card from '../components/Card';

export const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <header className="max-w-6xl mx-auto mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">대시보드</h1>
        <div className="text-sm text-gray-600">환영합니다, 사용자님</div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <h2 className="text-lg font-medium">프로필</h2>
          <p className="text-sm text-gray-600 mt-2">사용자 정보 및 계정 설정</p>
        </Card>

        <Card>
          <h2 className="text-lg font-medium">활동</h2>
          <p className="text-sm text-gray-600 mt-2">최근 활동 및 알림</p>
        </Card>

        <Card>
          <h2 className="text-lg font-medium">설정</h2>
          <p className="text-sm text-gray-600 mt-2">앱 설정 및 환경설정</p>
        </Card>
      </main>
    </div>
  );
};

export default Dashboard;

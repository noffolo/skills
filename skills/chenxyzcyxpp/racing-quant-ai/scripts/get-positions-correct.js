const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

/**
 * 根据策略名称从strategy_information表查询strategy_table
 * @param {string} strategyName - 策略名称（支持strategy_name_cn模糊匹配）
 * @returns {Promise<{strategyNameCn: string, strategyTable: string, strategyDesc: string}|null>}
 */
function findStrategyTable(strategyName) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      // 使用模糊匹配查询策略
      const query = `SELECT strategy_name_cn, strategy_table, strategy_desc, strategy_name 
                     FROM strategy_information 
                     WHERE strategy_name_cn LIKE ? OR strategy_name LIKE ?
                     LIMIT 5`;
      const likePattern = `%${strategyName}%`;
      connection.query(query, [likePattern, likePattern], (err, results) => {
        if (err) {
          reject(err);
          connection.end();
          return;
        }
        if (results.length === 0) {
          resolve(null);
          connection.end();
          return;
        }
        // 如果只有一个结果，直接返回；如果有多个，返回第一个并提示
        resolve({
          strategyNameCn: results[0].strategy_name_cn,
          strategyTable: results[0].strategy_table,
          strategyDesc: results[0].strategy_desc,
          strategyName: results[0].strategy_name,
          allMatches: results
        });
        connection.end();
      });
    });
  });
}

/**
 * 从指定策略表获取最新持仓
 * @param {string} tableName - 策略持仓表名
 * @param {number} limit - 返回持仓数量限制
 * @returns {Promise<{latestDate: string, positions: Array}>}
 */
function getLatestPositions(tableName, limit = 20) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      // 获取最新一期日期
      const dateQuery = `SELECT DISTINCT trade_date FROM ${tableName} ORDER BY trade_date DESC LIMIT 1`;
      connection.query(dateQuery, (err, dateResults) => {
        if (err) {
          reject(err);
          connection.end();
          return;
        }
        if (dateResults.length === 0) {
          resolve({ latestDate: null, positions: [] });
          connection.end();
          return;
        }
        const latestDate = dateResults[0].trade_date;
        // 获取最新一期持仓
        const posQuery = `SELECT trading_info FROM ${tableName} WHERE trade_date = ?`;
        connection.query(posQuery, [latestDate], (err, posResults) => {
          if (err) {
            reject(err);
            connection.end();
            return;
          }
          if (posResults.length === 0) {
            resolve({ latestDate, positions: [] });
            connection.end();
            return;
          }
          // 转成数组: {code: weight} -> [{code, weight}]
          const tradingInfo = posResults[0].trading_info;
          const positions = Object.entries(tradingInfo)
            .map(([code, weight]) => ({ stock_code: code, weight: Number(weight) }))
            .sort((a, b) => b.weight - a.weight)
            .slice(0, limit);
          resolve({
            latestDate,
            positions
          });
          connection.end();
        });
      });
    });
  });
}

// 主函数
async function main() {
  // 获取命令行参数
  const args = process.argv.slice(2);
  const strategyName = args[0];
  const limit = parseInt(args[1]) || 20;

  if (!strategyName) {
    console.log('用法: node get-positions-correct.js <策略名称> [持仓数量]');
    console.log('示例: node get-positions-correct.js "短周期机器学习" 20');
    console.log('      node get-positions-correct.js "趋势增强" 10');
    console.log('\n提示: 如果不确定策略名称，可以先运行: node list-recommended.js');
    process.exit(1);
  }

  try {
    // 第一步：根据策略名称查询strategy_table
    console.log(`🔍 正在查找策略: "${strategyName}"...\n`);
    const strategyInfo = await findStrategyTable(strategyName);

    if (!strategyInfo) {
      console.error(`❌ 未找到匹配的策略: "${strategyName}"`);
      console.log('\n提示: 使用更通用的关键词重试，或先运行: node list-recommended.js');
      process.exit(1);
    }

    // 如果匹配到多个策略，显示提示
    if (strategyInfo.allMatches && strategyInfo.allMatches.length > 1) {
      console.log(`⚠️  找到 ${strategyInfo.allMatches.length} 个匹配策略，使用第一个:\n`);
      strategyInfo.allMatches.forEach((match, i) => {
        const marker = i === 0 ? '✓' : ' ';
        console.log(`  [${marker}] ${match.strategy_name_cn}`);
        console.log(`      表名: ${match.strategy_table}`);
      });
      console.log();
    }

    console.log(`✅ 找到策略: ${strategyInfo.strategyNameCn}`);
    console.log(`📋 策略描述: ${strategyInfo.strategyDesc || '暂无描述'}`);
    console.log(`📊 持仓表名: ${strategyInfo.strategyTable}\n`);

    // 第二步：获取持仓数据
    const result = await getLatestPositions(strategyInfo.strategyTable, limit);

    if (!result.latestDate) {
      console.log('⚠️ 该策略暂无持仓数据');
      process.exit(0);
    }

    console.log(`📅 最新持仓日期: ${result.latestDate}`);
    console.log(`📈 持仓数量: ${result.positions.length} 只\n`);
    console.log(`持仓明细:\n`);
    result.positions.forEach((pos, i) => {
      console.log(`${String(i+1).padStart(2)}. ${pos.stock_code} - 权重: ${(pos.weight * 100).toFixed(2)}%`);
    });

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();

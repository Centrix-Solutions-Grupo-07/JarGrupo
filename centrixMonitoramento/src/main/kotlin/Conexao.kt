import org.apache.commons.dbcp2.BasicDataSource
import org.springframework.jdbc.core.JdbcTemplate

object Conexao {
    var jdbcTemplate: JdbcTemplate? = null
        get(){
            if(field == null){
                val dataSource = BasicDataSource()
                dataSource.url = "jdbc:mysql://localhost?serverTimezone=UTC"
                dataSource.username = "root"
                dataSource.password = "38762"
                val novoJdbcTemplate = JdbcTemplate(dataSource)
                field = novoJdbcTemplate
                println("////Login no banco bem sucedido!\\\\")

                jdbcTemplate!!.execute("""
                  create database if not exists centrix
              """)
                jdbcTemplate!!.execute("""
                  use Centrix
              """)
            }
            return field
        }

}